from typing import Literal, Dict, Tuple
from PySide6.QtWidgets import QSizePolicy

SizePolicyTypes = Literal[
    "fixed", 
    "minimum", 
    "maximum", 
    "preferred", 
    "expanding", 
    "min_expanding", 
    "ignored"
]

class SizePolicy:
    """
    Abstracción de QSizePolicy.Policy para usar cadenas simples.
    """

    FIXED           : QSizePolicy.Policy = QSizePolicy.Policy.Fixed
    MINIMUM         : QSizePolicy.Policy = QSizePolicy.Policy.Minimum
    MAXIMUM         : QSizePolicy.Policy = QSizePolicy.Policy.Maximum
    PREFERRED       : QSizePolicy.Policy = QSizePolicy.Policy.Preferred
    EXPANDING       : QSizePolicy.Policy = QSizePolicy.Policy.Expanding
    MIN_EXPANDING   : QSizePolicy.Policy = QSizePolicy.Policy.MinimumExpanding
    IGNORED         : QSizePolicy.Policy = QSizePolicy.Policy.Ignored


    _POLICY_MAP: Dict[str, QSizePolicy.Policy] = {
        "fixed": FIXED,
        "minimum": MINIMUM,
        "maximum": MAXIMUM,
        "preferred": PREFERRED,
        "expanding": EXPANDING,
        "min_expanding": MIN_EXPANDING,
        "ignored": IGNORED,
    }

    @classmethod
    def get_policy(cls, policy_string: SizePolicyTypes) -> QSizePolicy.Policy:
        """
        Convierte una cadena de política de tamaño a la bandera de Qt (QSizePolicy.Policy).
        """
       
        return cls._POLICY_MAP.get(policy_string, cls.PREFERRED)

    @classmethod
    def get(
        cls, 
        policy_def: SizePolicyTypes | Tuple[SizePolicyTypes, SizePolicyTypes]
    ) -> QSizePolicy:
        """
        Método de conveniencia para obtener un objeto QSizePolicy.
        
        Acepta:
        1. Una sola cadena (Ej: "expanding"): Aplica esa política a ambas dimensiones.
        2. Una tupla de dos cadenas (Ej: ("expanding", "fixed")): Horizontal, Vertical.
        """
        
        if isinstance(policy_def, str):

            qt_policy = cls.get_policy(policy_def)

            return QSizePolicy(qt_policy, qt_policy)
        
        elif isinstance(policy_def, tuple) and len(policy_def) == 2:

            horiz_policy, vert_policy = [cls.get_policy(pol) for pol in policy_def]

            return QSizePolicy(horiz_policy, vert_policy)

        return QSizePolicy(cls.PREFERRED, cls.PREFERRED)
