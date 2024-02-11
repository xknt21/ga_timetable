import random
import statistics  #数理統計関数→数値（Real型）データを数学的に統計計算するための関数を提供
import copy


##########定数の定義################
GENETIC_NUMBER = 25    #時間割のコマ数
INDIVIDUAL_NUMBER = 20 #集団の数
TABLE_ROW = 5          #時間割の行数
MAX_GENERATION = 1000   #世代数
ELITE_NUMBER = 10       #残すエリートの数
PENALTY_NUMBER = 100    #一つの曜日に同じ教科が複数ある場合、評価関数の値（stdの値）に100追加することによって、淘汰する

############クラスの定義#################

class Time_table:  #時間割クラスの定義
  def __init__(self,table,w_sd):
    self.table = table  #教科(Subjectクラス)のリスト
    self.w_sd = w_sd    #時間割の評価値

class Subject:
    def __init__(self,name,weight,distance,homework,test,stamina,mental):
       self.name = name         #教科名
       self.weight = weight     #教科の重量,４段階
       self.distance = distance #移動教室　3段階（有る、半分だけ、無い）
       self.homework = homework #宿題　３段階
       self.test = test         #授業前テスト　有るor無い
       self.stamina = stamina   #体力　要るor要らない
       self.mental = mental     #精神力　3段階
    
def calc_day_ave(lists):  #1つの時間割の評価値を求める（曜日ごとの負荷の計の標準偏差）
  w_list=[]
  d_list=[]
  h_list=[]
  t_list=[]
  s_list=[]
  m_list=[]
  sum = []
  m = 0
  for w in lists:
    w_list.append(w.weight)   #append...リストに要素を追加するためのメソッド
    d_list.append(w.distance)
    h_list.append(w.homework)
    t_list.append(w.test)
    s_list.append(w.stamina)
    m_list.append(w.mental)
  for i in range(TABLE_ROW):
    for k in range(TABLE_ROW*i,TABLE_ROW*(i+1)):
      m += w_list[k]
      m += d_list[k]
      m += h_list[k]
      m += t_list[k]
      m += s_list[k]
      m += m_list[k]
    sum.append(round(m,2))
    m=0
    if any(lists[TABLE_ROW*i:TABLE_ROW*(i+1)].count(t)>1 for t in lists[TABLE_ROW*i:TABLE_ROW*(i+1)]):    #もし一つの曜日に同じ教科が複数あるなら
       sum[i] += PENALTY_NUMBER    #その曜日の合計重量に100足すことで淘汰されるようにする
    

  
  return sum

def data_dis(lists): #1つの時間割リストを表示  
  for num in range(TABLE_ROW):
    print(lists[num].name,lists[TABLE_ROW+num].name,lists[2*TABLE_ROW+num].name,\
          lists[3*TABLE_ROW+num].name,lists[4*TABLE_ROW+num].name,end = " ",file=f)
    print(lists[num].weight,lists[TABLE_ROW+num].weight,lists[2*TABLE_ROW+num].weight,\
          lists[3*TABLE_ROW+num].weight,lists[4*TABLE_ROW+num].weight,end = "  ",file=f)   
    print(lists[num].distance,lists[TABLE_ROW+num].distance,lists[2*TABLE_ROW+num].distance,\
          lists[3*TABLE_ROW+num].distance,lists[4*TABLE_ROW+num].distance,end = "  ",file=f)   
    print(lists[num].homework,lists[TABLE_ROW+num].homework,lists[2*TABLE_ROW+num].homework,\
          lists[3*TABLE_ROW+num].homework,lists[4*TABLE_ROW+num].homework,end = "  ",file=f)   
    print(lists[num].test,lists[TABLE_ROW+num].test,lists[2*TABLE_ROW+num].test,\
          lists[3*TABLE_ROW+num].test,lists[4*TABLE_ROW+num].test,end = "  ",file=f)   
    print(lists[num].stamina,lists[TABLE_ROW+num].stamina,lists[2*TABLE_ROW+num].stamina,\
          lists[3*TABLE_ROW+num].stamina,lists[4*TABLE_ROW+num].stamina,end = "  ",file=f)
    print(lists[num].mental,lists[TABLE_ROW+num].mental,lists[2*TABLE_ROW+num].mental,\
          lists[3*TABLE_ROW+num].mental,lists[4*TABLE_ROW+num].mental,file=f)    
  print("----------------------------------------------",file=f)
  print(calc_day_ave(lists),"  std=",round(statistics.stdev(calc_day_ave(lists)),2),file=f)
  print("----------------------------------------------",file=f)

def table_dis(list):  #時間割集団のリストを表示
    for num in range(len(list)):
        data_dis(list[num].table)
    
def alternation_of_generations(tables):  #世代交代を行い、表示する関数
    new_table = sorted(tables,key=lambda u: u.w_sd)  #標準偏差をkeyにソート
    del new_table[ELITE_NUMBER-INDIVIDUAL_NUMBER:]   #後ろから15個削除（ELITE_NUMBER-INDIVIDUAL_NUMBER=-15)
    for num in range(INDIVIDUAL_NUMBER-ELITE_NUMBER): 
        g = copy.copy(random.sample(Genome_lists,len(Genome_lists)))
        table = Time_table(g, round(statistics.stdev(calc_day_ave(g)),2))
        new_table.append(table)
    table_dis(new_table)    
    return new_table
    
###################ここまでが各関数の定義############################
f = open('GA_timetable.txt','w')

###################教科のインスタンス生成###################
jap1 = Subject("現文",2,0,3,1,0,1)
jap2 = Subject("古典",2,0,3,1,0,2)
math1 = Subject("特論",1,0,3,0,0,2)
math2 = Subject("数II",1,1,3,0,0,3)
eng1 = Subject("英理",4,0,2,1,0,2)
eng2 = Subject("英表",4,1,2,1,0,1)
physics = Subject("物理",3,2,3,0,0,2)
chem = Subject("化学",3,0,0,1,0,2)
his = Subject("世史",3,0,0,0,0,1)
geog = Subject("地理",4,0,1,0,0,2)
physical = Subject("体育",2,2,0,0,1,1)
judo = Subject("柔道",4,2,0,0,1,1)
health = Subject("保健",1,0,0,0,0,1)
home = Subject("家庭",2,0,0,0,0,1)
LHR = Subject("LHR",1,0,0,0,0,0)



##########################初期集団の生成########################
Genome_lists = [jap1,jap2,jap2,math1,math1,math2,math2,math2,eng1,eng1,eng2,\
                physics,physics,chem,chem,his,his,geog,geog,physical,physical,judo,health,home,LHR]

Genome_table = []  #ここにTime_tableクラスのインスタンスをINDIVIDUAL_NUMBERの数だけ格納する。すなわち時間割の集団を作る
for i in range(INDIVIDUAL_NUMBER):  
    g = copy.copy(random.sample(Genome_lists,len(Genome_lists)))
    table = Time_table(g, round(statistics.stdev(calc_day_ave(g)),2))
    
    Genome_table.append(table)
    
table_dis(Genome_table) #初期集団を表示
print("\n=======================初期集団生成完了=========================\n\n",file=f)


##########################世代交代############################
for i in range(MAX_GENERATION):
    print("\nーーーーーーーーーーーーーーーー第",i+1,"世代ーーーーーーーーーーーーーーー\n",file=f)
    Genome_table = alternation_of_generations(Genome_table)

f.close()



