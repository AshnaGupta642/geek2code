from pydantic import BaseModel, Field


class MemoryReconstructionStartRequest(BaseModel):
    patient_id: int = Field(gt=0)
    memory_id: int = Field(gt=0)
    language: str = Field(default="en", min_length=2, max_length=10)


class MemoryReconstructionStartResponse(BaseModel):
    session_id: str
    current_stage: str
    question: str


class MemoryReconstructionAnswerRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    patient_id: int = Field(gt=0)
    memory_id: int = Field(gt=0)
    answer_text: str = Field(min_length=1)


class AnswerAnalysis(BaseModel):
    recognized: bool
    confidence: float = Field(ge=0, le=1)
    extracted_information: list[str] = Field(default_factory=list)


class MemoryReconstructionAnswerResponse(BaseModel):
    session_id: str
    answer_analysis: AnswerAnalysis
    next_stage: str
    next_question: str
    updated_context: str