from sqlmodel import Field, SQLModel


class VulnerabilitieWorkstationModel(SQLModel, table=True):
    __tablename__ = "vulnerabilitie_workstation"

##si eliminas un workstation o una vulnerabilitie entonces lo que hara la bd es eliminar tambien los registros que se encuentren en esta tabla, el CASCADE esta en la migracion "a1231e359665_create_vulnerabilitie_workstation_" por si quieres verla
    workstation_id: str = Field(
        foreign_key="workstations.id",
        primary_key=True,
    )

    vulnerabilitie_id: str = Field(
        foreign_key="vulnerabilities.id",
        primary_key=True,
    )