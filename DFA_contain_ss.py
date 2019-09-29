
#DFA : { Q, A, hamchuyen, q0, F}. Trong do A = {0, 1} - ngon ngu xau nhi phan
#DFA xay dung nn gom cac tu chua xau con : a1 .... ak
# -> Q gom k + 1 trang thai : q0, q1,..., qk
# -> trang thai bat dau : q0
# -> trang thai ket thuc : F = {qk}
# Thuat toan tim ham chuyen duoi dang bang anh xa


from pythomata.dfa import DFA
import pydot


class BiDict :
        def __init__(self, d : dict):
                self.key2value = d
                self.value2key = {}
                for k,v in d.items():
                        self.value2key[v] = k
                        
        def list_key(self):
                return list(self.key2value.keys())
        
        def list_val(self):
                return list(self.key2value.values())
        
        def _get_val(self, key):
                return self.key2value[key]
        
        def _get_key(self, val):
                return self.value2key[val]
        
        def _iter_key(self):
                return iter(self.key2value.keys())
        
        def _iter_val(self):
                return iter(self.value2key.keys())


def del1_prefix(str):
        return str[1:]


def DFAss_hashmap(A, substring):
        n = len(substring)
        # tap trang thai
        Q = []
        for i in range(n+1):
                state = 'q' + str(i)
                Q.append(state)
                
        # qi ung voi xau hien tai theo chieu a1 -> a(i+1)
        state_str = dict(zip(Q, [substring[:i] for i in range(n+1)]))
        state_str = BiDict(state_str)
        
        # bang anh xa hashmap
        dict_map = dict(zip(Q, [[] for x in range(n+1)]))
        
        for q in state_str._iter_key():
                # Trang thai cuoi lap ve chinh no
                if q == Q[n]:
                        dict_map[q] += [q, q]
                        continue
                
                s = state_str._get_val(q)
                for a in A :
                        s_loop = s + str(a)
                        while(True):
                                if s_loop in state_str.list_val():
                                        dict_map[q].append(state_str._get_key(s_loop))
                                        break
                                else :
                                        s_loop = del1_prefix(s_loop)
        return Q, dict_map


        # test ham chuyen
        #substring = '11001'
        #A = ['0','1']
        #res = DFAss_hashmap(A, substring)

# Input
substring = '1001010'
#substring = '10'
#substring = '101'
#substring = '1010'

A = ['0','1']
Q, hashmap = DFAss_hashmap(A, substring)


alphabet = set(A)
states = set(Q)
initial_state = Q[0]
accepting_states = {Q[-1]}
transition_function = {}
for key,value in hashmap.items() :
        dict_trans = {}
        for i in range(len(value)):
                dict_trans[A[i]] = value[i]
        transition_function[key] = dict_trans
dfa = DFA(states, alphabet, initial_state, accepting_states, transition_function)

# Main
filepath = "./diagram1"
try :
        dfa.to_dot(filepath)
except: 
        pass
(graph,) = pydot.graph_from_dot_file('./diagram1')
graph.write_png('diagram1.png')