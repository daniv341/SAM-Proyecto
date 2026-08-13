# alembic/models.py
#
# Registro central de modelos ORM.
# Alembic necesita que todos los modelos estén importados en memoria
# para poder comparar el estado actual de la BD con el código
# y generar las migraciones correctas con --autogenerate.
#
# REGLA: cada vez que crees una nueva entidad, agregá su modelo aquí.

#from src.player.infrastructure.repositories.player_model import PlayerModel          # noqa: F401

from src.user.infrastructure.repositories.user_model import UserModel              # noqa: F401
from src.workstation.infrastructure.repositories.workstation_model import WorkstationModel  # noqa: F401
from src.vulnerabilitie.infrastructure.repositories.vulnerabilitie_model import VulnerabilitieModel  # noqa: F401

# Próximas entidades (descomentá cuando las crees):
# from src.tournament.infrastructure.repositories.tournament_model import TournamentModel  # noqa: F401
# from src.match.infrastructure.repositories.match_model import MatchModel                 # noqa: F401
