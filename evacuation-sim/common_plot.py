
import matplotlib.pyplot as plt

def plotgrid(myarray, highlight_roads=[], house_status={}, step_num=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim([-0.5, myarray.shape[1] + 5])
    ax.set_ylim([-0.5, myarray.shape[0] + 0.5])
    plt.axis('off')

    emoji_map = {
        1: "🌲",  # Tree
        2: "🟡",  # Just Ignited
        3: "🟩",  # Safe zone
        4: "⬛",  # Road
        5: "🔴",  # Burning
        6: "🟥",  # Burned
        22: "🏠", # House (later overwritten by pink square emoji)
    }

    for y in range(myarray.shape[0]):
        for x in range(myarray.shape[1]):
            val = myarray[y][x]
            if val == 22:
                ax.text(x, myarray.shape[0] - y - 1, "🟪", fontsize=18, ha='center', va='center')
            elif val in emoji_map:
                ax.text(x, myarray.shape[0] - y - 1, emoji_map[val], fontsize=18, ha='center', va='center')

    for (y, x) in highlight_roads:
        ax.text(x, myarray.shape[0] - y - 1, "🚑", fontsize=18, ha='center', va='center')

    for (y, x), step in house_status.items():
        ax.text(x, myarray.shape[0] - y - 1, f"{step}", color='black', fontsize=8, ha='center', va='center')

    legend_start_y = 9
    legend = [
        "🌲 Tree",
        "🟡 Just Ignited",
        "🔴 Burning",
        "🟥 Burned",
        "⬛ Road",
        "🟪 House (Pink Square)",
        "🚑 EMS Path"
    ]
    for i, text_line in enumerate(legend):
        ax.text(myarray.shape[1] + 1, legend_start_y - i * 0.5, text_line, fontsize=10)

    if step_num is not None:
        ax.text(myarray.shape[1] + 1, legend_start_y - len(legend) * 0.5 - 0.5, f"🕒 Time: {step_num} min", fontsize=10, fontweight='bold')

    plt.show()

