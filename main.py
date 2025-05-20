import argparse
import matplotlib.pyplot as plt

positions, strikes, points = [], [], []
n = int(input("Number of options : "))
print("Enter : quantity | call/put | strike | cost")

while n>0:
    cmd = input("> ").split()
    parser = argparse.ArgumentParser()
    parser.add_argument("qty" , type=int)
    parser.add_argument("type" , choices=["call" , "put"])
    parser.add_argument("strike" , type=float)
    parser.add_argument("cost" , type=float)
    positions.append(parser.parse_args(cmd))
    n -= 1

for i in positions:
    strikes.append(i.strike)

strikes = sorted(strikes)
strikes.append(strikes[-1]+5)
strikes.append(strikes[0]-5)

strikes = set(strikes)

underlying = input("Enter underlying contracts (quantity | price) : ")
underlying = underlying.split(" ")
underlying = [int(a) for a in underlying]


for strike in strikes:
    cost = 0.00
    for position in positions:
        if position.type == "call":
            if strike <= position.strike:
                cost -= position.qty * position.cost
            else:
                cost += position.qty * (strike - position.strike - position.cost)
        else:
            if strike >= position.strike:
                cost -= position.qty * position.cost
            else:
                cost += position.qty * (position.strike - strike - position.cost)
    points.append((strike,(round(cost,2))))

points.sort()

x_vals = [point[0] for point in points]
y_vals = [((underlying[0]*(point[0]-underlying[1]))+point[1]) for point in points]

inner_x = x_vals[1:-1]
inner_y = y_vals[1:-1]

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, linestyle='-', color='blue', label='P&L')

plt.scatter(inner_x, inner_y, color='blue', zorder=5)

plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

plt.title("Options Strategy Payoff Diagram")
plt.xlabel("Underlying Price at Expiry (Strike)")
plt.ylabel("Net Profit / Loss")
plt.grid(True)
plt.legend()
plt.show()

