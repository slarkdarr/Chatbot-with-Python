class LevDist:
    def __init__(self, stra, strb):
        self.a = stra
        self.b = strb
        self.lena = len(self.a)
        self.lenb = len(self.b)
        self.quickLev = [[None for j in range(self.lenb+1)] for i in range(self.lena+1)]
        self.dist = self.lev(self.lena, self.lenb)
        self.sim = 1-self.dist/max(self.lena, self.lenb)

    def lev(self, i, j):
        if min(i, j) == 0:
            self.quickLev[i][j] = max(i, j)
            return self.quickLev[i][j]
        else:
            qlev = self.quickLev[i][j]
            if (qlev != None):
                return qlev
            else:
                self.quickLev[i][j] = min(self.lev(i-1, j)+1, self.lev(i, j-1)+1, self.lev(i-1, j-1) + (1 if self.a[i-1] != self.b[j-1] else 0))
                return self.quickLev[i][j]