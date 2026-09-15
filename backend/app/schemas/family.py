from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, computed_field, field_validator


def _blank_to_none(value):
    if isinstance(value, str) and not value.strip():
        return None
    return value


class FamilyMemberCreate(BaseModel):
    name: str
    relationship: str = Field(validation_alias=AliasChoices("relationship", "rel"))
    phone: str | None = Field(default=None, validation_alias=AliasChoices("phone"))
    photo_url: str | None = Field(default=None, validation_alias=AliasChoices("photo_url", "photo"))
    is_caregiver: bool = False
    user_id: int | None = None
    is_emergency: bool | None = Field(default=None, validation_alias=AliasChoices("is_emergency", "isEmergency"))
    is_primary: bool | None = Field(default=None, validation_alias=AliasChoices("is_primary", "isPrimary"))

    @field_validator("phone", "photo_url", mode="before")
    @classmethod
    def empty_optional(cls, value):
        return _blank_to_none(value)


class FamilyMemberUpdate(BaseModel):
    name: str | None = None
    relationship: str | None = Field(default=None, validation_alias=AliasChoices("relationship", "rel"))
    phone: str | None = None
    photo_url: str | None = Field(default=None, validation_alias=AliasChoices("photo_url", "photo"))
    is_caregiver: bool | None = None
    is_active: bool | None = None
    user_id: int | None = None
    is_emergency: bool | None = Field(default=None, validation_alias=AliasChoices("is_emergency", "isEmergency"))
    is_primary: bool | None = Field(default=None, validation_alias=AliasChoices("is_primary", "isPrimary"))

    @field_validator("phone", "photo_url", "relationship", "name", mode="before")
    @classmethod
    def empty_optional(cls, value):
        return _blank_to_none(value)


class FamilyMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    patient_id: int
    user_id: int | None
    name: str
    relationship: str
    phone: str | None
    photo_url: str | None
    is_caregiver: bool
    is_active: bool
    created_at: datetime

    @computed_field
    @property
    def rel(self) -> str:
        return self.relationship

    @computed_field
    @property
    def photo(self) -> str | None:
        return self.photo_url

    @computed_field
    @property
    def isEmergency(self) -> bool:
        return self.is_caregiver

    @computed_field
    @property
    def isPrimary(self) -> bool:
        return self.is_caregiver
