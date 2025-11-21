import matplotlib.pyplot as plt
from IPython import display

plt.ion()
fig, ax = plt.subplots()

def plot(scores, mean_scores):
    ax.clear()
    ax.plot(scores, label='Score', color='b', alpha=0.7)
    ax.plot(mean_scores, label='Mean Score', color='r')
    ax.set_title('Snake Game Training')
    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Score')
    ax.legend()
    ax.text(len(scores)-1, scores[-1], f'Score: {scores[-1]:.2f}', verticalalignment='bottom')
    ax.text(len(mean_scores)-1, mean_scores[-1], f'Mean: {mean_scores[-1]:.2f}', verticalalignment='bottom')
    ax.grid(True)
    plt.pause(0.1)
    display.display(fig)
