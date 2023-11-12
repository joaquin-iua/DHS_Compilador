class Temps:
    _tempsList = []
    _temp = 0
    @property
    def t(self):
        Temps._temp += 1
        self._tempsList.append(Temps._temp)
        return f't{Temps._tempsList[-1]} '

    @property
    def previousT(self):
        return f't{Temps._tempsList[-2]}'

    @property
    def currentT(self):
        return f't{Temps._tempsList[-1]}'