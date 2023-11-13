int x = 10;
double c;
int z;

{
    int x;
    int y = 2;
    {
        int z;
        {
            int x;
            z = x;
        }
    }
}

x = -10;
y = -x + 5 / 3 + 1;

z = x + y;

y = 0;

int p, q, r, s;

int a, b = 0, c = 2, d = 5;

while (x < 10) {
    z = y;
    a = b + c;
}

while (x < 10)
    a = b + c;

if (5 + 3 > 4 + 2)
    a = 3;

int func(int x, int t);

int func(int x, int t) {
    return x + t;
}

b = func(3, 4);
int bb = func(a, b);

