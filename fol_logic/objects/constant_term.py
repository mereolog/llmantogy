from fol_logic.objects.term import Term


class ConstantTerm(Term):
    registry = dict()
    
    def __init__(self, origin_value: object, origin_type=str):
        super().__init__(origin_value=origin_value, origin_type=origin_type)
        Term.registry[origin_value] = self
    