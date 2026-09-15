import cv2
import json
import numpy as np

from insightface.app import FaceAnalysis


class FaceRecognitionService:

    def __init__(self):
        self.app = FaceAnalysis(name="buffalo_l")

        # CPU
        self.app.prepare(
            ctx_id=-1,
            det_size=(640, 640)
        )

    def get_embedding(self, image_bytes: bytes):

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:
            raise ValueError("Invalid image")

        faces = self.app.get(image)

        if len(faces) == 0:
            return None

        # If multiple faces are detected,
        # choose the largest face.
        face = max(
            faces,
            key=lambda f:
            (f.bbox[2] - f.bbox[0]) *
            (f.bbox[3] - f.bbox[1])
        )

        embedding = face.embedding

        # Normalize
        embedding = embedding / np.linalg.norm(embedding)

        return embedding.tolist()

    def calculate_similarity(
        self,
        embedding1,
        embedding2
    ):

        a = np.array(
            embedding1,
            dtype=np.float32
        )

        b = np.array(
            embedding2,
            dtype=np.float32
        )

        return float(
            np.dot(a, b) /
            (
                np.linalg.norm(a) *
                np.linalg.norm(b)
            )
        )

    def find_best_match(
        self,
        query_embedding,
        profiles,
        threshold=0.40
    ):

        best_profile = None
        best_score = -1.0

        for profile in profiles:

            if not profile.embedding_reference:
                continue

            try:
                stored_embedding = json.loads(
                    profile.embedding_reference
                )
            except Exception:
                continue

            score = self.calculate_similarity(
                query_embedding,
                stored_embedding
            )

            if score > best_score:
                best_score = score
                best_profile = profile

        if (
            best_profile is not None
            and best_score >= threshold
        ):

            return {
                "family_member_id":
                    best_profile.family_member_id,

                "person_name":
                    best_profile.person_name,

                "confidence":
                    round(best_score, 4),

                "matched": True
            }

        return {
            "family_member_id": None,
            "person_name": None,
            "confidence":
                round(best_score, 4)
                if best_score >= 0
                else None,
            "matched": False
        }


face_service = FaceRecognitionService()