import matplotlib.pyplot as plt
import numpy as np

# データの生成
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# サブプロットを作成
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

# 上のグラフをプロット
ax1.plot(x, y1, 'g-', label='Sin(X)')
ax1.set_ylabel('Sin(X)')
ax1.tick_params(axis='x', labelbottom=False)  # x軸ラベルを省略
ax1.tick_params(axis='both', direction='in')  # メモリ線を内側に
ax1.legend(loc='upper right')

# 下のグラフをプロット
ax2.plot(x, y2, 'b-', label='Cos(X)')
ax2.set_xlabel('X data')
ax2.set_ylabel('Cos(X)')
ax2.tick_params(axis='both', direction='in')  # メモリ線を内側に
ax2.legend(loc='upper right')

# プロットを表示
plt.tight_layout()
plt.show()


