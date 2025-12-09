# app.py
import streamlit as st
from utils.data_loader import load_all_data

st.set_page_config(
    page_title="都市救急システミックリスク・ダッシュボード",
    layout="wide"
)

st.title("🚑 都市救急 システミックリスク・ダッシュボード")
st.markdown("### QUBO × 救急医療 × 相関ネットワークによる次世代アナリティクス")

# app.py
df_mesh, df_zones, df_systemic, df_comm, df_comm_mix = load_all_data()

st.success("データ読込完了！")

st.markdown("""
---
## 📌 このアプリでできること

### 1. ゾーン同士の相関ネットワーク（120×120）可視化  
QUBO の “Vgg'” をヒートマップ＋ネットワーク図で表示します。

### 2. QUBO vs Rank の比較分析  
どの病院が QUBO によって救われ、どの病院が悪化するのかを一目で確認できます。

### 3. Systemic Risk Map  
“救急連鎖崩壊リスク” を地図に投影します。

### 4. シナリオ・シミュレーション  
- 大病院停止  
- 大規模イベント  
- 高齢化  
などの仮想シナリオを計算します。

### 5. 病院別リスクスコア  
- SSS（Systemic Stress Score）  
- CDS（Cluster Dependency Score）  
- SE（Shock Elasticity）

---
### 左のサイドバーから機能を選択してください。
""")
