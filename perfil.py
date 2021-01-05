
class Perfil:

    file = None
    def __init__(self,file):
        self.sesion_user = None
        self.sesion_pass = None
        self.espera = None
        self.lim_dia_foll = None #limite diario para seguir
        self.lim_dia_unfoll = None #limite cada media hora para seguir
        self.lim_hora_foll = None #limite diario par deajra de seguir
        self.lim_hora_unfoll = None #limite cada 10 minutos para dejar de seguir
        self.perfiles_seguir = None #lista de perfelies donde buscar seguidores
        self.perfiles_dejar = None #lista de perfiles para dejar de seguir
        self.solo_seguidores = None #solo deja de seguir, los perfiles que no te siguen
        self.ratio_dejar = None #usa una relacion entre seguidores y seguidos para dejar 1.3 quiere decir que si tiene mas de 30% seguidores que seguidos lo va a dejar
        self.limite_sup_dejar = None #si tiene mas de n seguidores lo dejar
        self.tiempo_min_dejar = None #cantidad de dias desde que se lo siguio hasta que s elo puede dejar de seguir
        self.file = file



print(Perfil)