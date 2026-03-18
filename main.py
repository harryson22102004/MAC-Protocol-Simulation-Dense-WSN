import random, statistics
 
class CSMACANode:
    def __init__(self, nid, cw_min=8, cw_max=64):
        self.id=nid; self.cw_min=cw_min; self.cw_max=cw_max
        self.backoff=random.randint(0,cw_min); self.collisions=0; self.sent=0
    def sense_channel(self, busy_prob): return random.random()<busy_prob
    def transmit(self, slot):
        if self.backoff>0: self.backoff-=1; return 'deferring'
        return 'transmitting'
    def on_collision(self):
        self.collisions+=1; self.cw_min=min(self.cw_min*2,self.cw_max)
        self.backoff=random.randint(0,self.cw_min)
    def on_success(self):
        self.sent+=1; self.cw_min=8; self.backoff=random.randint(0,self.cw_min)
 
def simulate_mac(n_nodes=20, n_slots=1000):
    nodes=[CSMACANode(i) for i in range(n_nodes)]
    stats={'collisions':0,'successes':0,'idle':0}
    for slot in range(n_slots):
        txing=[n for n in nodes if n.transmit(slot)=='transmitting']
        if len(txing)==0: stats['idle']+=1
        elif len(txing)==1: txing[0].on_success(); stats['successes']+=1
        else:
            for n in txing: n.on_collision()
            stats['collisions']+=1
    total=stats['collisions']+stats['successes']+stats['idle']
    print(f"Nodes: {n_nodes} | Slots: {n_slots}")
    print(f"Success rate: {stats['successes']/total:.2%}")
    print(f"Collision rate: {stats['collisions']/total:.2%}")
    print(f"Total sent: {sum(n.sent for n in nodes)}")
 
simulate_mac(n_nodes=15, n_slots=2000
