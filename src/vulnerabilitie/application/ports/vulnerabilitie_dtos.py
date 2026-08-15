from datetime import datetime
from pydantic import BaseModel, field_validator

from src.vulnerabilitie.domain.vulnerabilitie import Severity

from src.vulnerabilitie.domain.vulnerabilitie_validate import Description, CVE


class CreateVulnerabilitieDTO(BaseModel):
    cve: str
    description: str | None = None
    severity: Severity
    url: str
    mitigation: bool

    @field_validator("cve")
    @classmethod
    def cve_must_be_valid(cls, v):
        return CVE(v).value

    @field_validator("description")
    @classmethod
    def description_must_be_valid(cls, v):
        return Description(v).value

class UpdateVulnerabilitieDTO(BaseModel):
    description: str | None = None
    mitigation: bool | None = None

    @field_validator("description")
    @classmethod
    def description_must_be_valid(cls, v):
        return Description(v).value


class VulnerabilitieResponseDTO(BaseModel):
    id: str
    cve: str
    description: str | None = None
    severity: Severity
    url: str
    mitigation: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class VulnerabilitieResponseShortDTO(BaseModel):
    id: str
    cve: str
    severity: Severity
    mitigation: bool

    model_config = {"from_attributes": True}

class VulnerabilitieListResponseDTO(BaseModel):
    vulnerabilities: list[VulnerabilitieResponseDTO]
    total: int
    skip: int
    limit: int
