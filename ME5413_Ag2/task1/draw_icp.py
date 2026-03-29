import matplotlib.pyplot as plt

with open(f"icp_result.txt") as f:
    res_line_lst = f.read().splitlines()

res_lst = [ round(eval(r),6) for r in res_line_lst]

title = "ICP Convergence Illustration"
x_label     =         "Iteration"
y_label     =        "Mean Error"


iter = list(range(1,len(res_lst)+1))
plt.figure(figsize=(16,9))
plt.plot(iter, res_lst, marker='o', linestyle='-', markersize=4)



plt.text(1, res_lst[1-1], f"(1, \n{res_lst[1-1]})",
         fontsize=10, ha = "center", va="bottom", color = "black")
plt.text(len(res_lst)+1, res_lst[-1], f"({len(res_lst)+1}, \n{res_lst[-1]})",
         fontsize=10, color = "black", ha = "center", va="bottom")

plt.rcParams.update({
    'font.family':'monospace',
    'font.stretch': 'condensed'
})

plt.xlim(-4, len(res_lst)+6)
plt.ylim(-0.1, res_lst[0]+0.3)


plt.title(title)
plt.xlabel(x_label)
plt.ylabel(y_label)

plt.grid(True)

file_name = "_".join(title.split(' '))
plt.savefig(f"{file_name}_final.png",dpi=800 )
plt.show()