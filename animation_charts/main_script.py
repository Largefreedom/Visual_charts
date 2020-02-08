#头文件加载
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import random

# 数据获取

url = 'https://gist.githubusercontent.com/johnburnmurdoch/4199dbe55095c3e13de8d5b2e5e5307a/raw/fa018b25c24b7b5f47fd0568937ff6c04e384786/city_populations'
df = pd.read_csv(url, usecols=['name', 'group', 'year', 'value'])

# 生成颜色代码函数
def randomcolor():
    colorlist = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color =''
    for i in range(6):
        color += random.choice(colorlist)
    return '#'+ color

#color_list:颜色代码列表，area_list获取地区列表
area_list = [i for i in set(df['group']))
color_list =[]
for i in range(len(area_list)):
    str_1 = randomcolor()
    color_list.append(str_1)


# 生成地区：颜色键值对，并且设置重新 Dataframe，以name为索引
colors =dict(zip(area_list_1,color_list))
#设置df_index为name，group为设置，to_dict设置为字典；
group_lk = df.set_index('name')['group'].to_dict()


#绘制条形图
fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(current_year):
    
    dff = df[df['year'].eq(current_year)].sort_values(by='value',ascending = True).tail(10)
    #横坐标清除
    ax.clear()
    ax.barh(dff['name'],dff['value'],color = [colors[group_lk[x]] for x in dff['name']])
    
    dx = dff['value'].max()/200
    for i ,(value,name) in enumerate(zip(dff['value'], dff['name'])):
        ax.text(value-dx,i,name,size=14,weight=600,ha ='right',va = 'bottom')
        ax.text(value-dx,i-.25,group_lk[name],size = 10,color ='#444444',ha ='right',va = 'baseline')
        ax.text(value+dx,i ,f'{value:,.0f}',size = 14,ha = 'left',va ='center')
    ax.text(1,0.4,current_year,transform = ax.transAxes,color ='#777777',size = 46,ha ='right',weight=800) 
    ax.text(0,1.06,'Popukation (throusands)',transform = ax.transAxes,size=12,color='#777777')
    
    # 小细节修饰
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x',colors='#777777',labelsize=12)
    ax.set_yticks([])
    ax.margins(0,0.01)
    ax.grid(which='major',axis='x',linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0,1.15,'The most populous cities in the word from 1500 to 2018',
           transform=ax.transAxes,size=24,weight=600,ha='left',va='top')
    ax.text(1,0,'by @pratapvardhan: crediet @jburnmurdoch',transform = ax.transAxes,color ='#777777',ha = 'right',
           bbox = dict(facecolor='white',alpha = 0.8,edgecolor='white'))
    
    plt.box(False)
 
 
# 由静态图生成动画效果图；
fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1900, 2019))
HTML(animator.to_jshtml()) 
