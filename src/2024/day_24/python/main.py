from enum import Enum

def and_oper(val1:int, val2:int) -> int:
    print(f'AND: {val1} & {val2} = {val1 & val2}')
    val = val1 & val2
    print(f'val = {val}')
    return val

def or_oper(val1:int, val2:int) -> int:
    print(f'OR : {val1} | {val2} = {val1 | val2}')
    return (val1 | val2)

def xor_oper(val1:int, val2:int) -> int:
    print(f'XOR: {val1} ^ {val2} = {val1 ^ val2}')
    return (val1 ^ val2)

class Oper(Enum):
    AND = ('AND', and_oper)
    OR  = ('OR', or_oper)
    XOR = ('XOR', xor_oper)

    def __call__(self, *args, **kwargs):
        self.value[1](*args, **kwargs)
    
    @staticmethod
    def get_enum(int_id:int):
        return {val.value[0]:val for val in Oper}[int_id]

Gate = tuple[str, str, Oper, str]

def main_part1(init_vals:[str, int], connections:list[Gate]):
    vals = init_vals.copy()
    gates = connections.copy()
    unresolved = len(gates)
    while gates:
        to_remove = []
        for gate in gates:
            if gate[0] in vals and gate[1] in vals:
                if gate[2] == Oper.AND:
                    val = vals[gate[0]] & vals[gate[1]]
                elif gate[2] == Oper.OR:
                    val = vals[gate[0]] | vals[gate[1]]
                else:
                    val = vals[gate[0]] ^ vals[gate[1]]
                vals[gate[3]] = val
                to_remove.append(gate)
        gates = [g for g in gates if g not in to_remove]
        if len(gates) == 0 or len(gates) == unresolved:
            break
        unresolved = len(gates)
    
    z_gates = [g for g in vals.keys() if g.startswith('z')]
    z_gates.sort()

    z_val = 0
    for idx, z in enumerate(z_gates):
        z_val += vals[z] * 2**idx
    
    print(z_val)

def find_gate_by_inputs(connections:list[Gate], in1:str, oper:Oper, in2:str=None) -> Gate:
    for c in connections:
        if c[2] != oper:
            continue
        if in2:
            if c[0] not in [in1, in2]:
                continue
            if c[1] not in [in1, in2]:
                continue
        else:
            if in1 not in [c[0], c[1]]:
                continue
        return c

def main_part2(connections:list[Gate]):
    conn_map = {c[3]:c for c in connections}
    z_ints = [int(c[1:]) for c in conn_map.keys() if c.startswith('z')]
    swaps_z = []
    for z_int in range(1,max(z_ints)):
        xor = find_gate_by_inputs(connections, f'x{z_int:02}', Oper.XOR, f'y{z_int:02}')
        z_gate = conn_map[f'z{z_int:02}']
        if z_gate[2] != Oper.XOR:
            print(z_int)
            swaps_z.append(z_gate[3])
            if z_gate[0].startswith('x') or z_gate[0].startswith('y'):
                zand = find_gate_by_inputs(connections,  f'x{z_int-1:02}', Oper.AND, f'y{z_int-1:02}')
                print(387, zand)
                left_or = find_gate_by_inputs(connections, zand[3], Oper.OR)
                print(389, left_or)
                total_xor = find_gate_by_inputs(connections, left_or[3], Oper.XOR)
                swaps_z.append(total_xor[3])
            else:
                gate2 = find_gate_by_inputs(connections, xor[3], Oper.XOR)
                print(399, gate2)
                swaps_z.append(gate2[3])
            continue
        if xor[3] not in [z_gate[0], z_gate[1]]:
            print(z_int)
            swaps_z.append(xor[3])
            zand = find_gate_by_inputs(connections,  f'x{z_int-1:02}', Oper.AND, f'y{z_int-1:02}')
            print(406, zand)
            left_or = find_gate_by_inputs(connections, zand[3], Oper.OR)
            print(408, left_or)
            total_xor = find_gate_by_inputs(connections, left_or[3], Oper.XOR)
            print(410, total_xor)
            if total_xor[0] == left_or[3]:
                swaps_z.append(total_xor[1])
            else:
                swaps_z.append(total_xor[0])
        
    print(','.join(sorted(swaps_z)))

def swap_gate(gate:Gate, idx:int, vals, orig_val:int) -> bool:
    v0 = vals[gate[0]]
    v1 = vals[gate[1]]
    if gate[2] == Oper.AND:
        if idx == 0:
            val = ((v0 + 1) % 2) & v1
        else:
            val = v0 & ((v1 + 1) % 2)
    elif gate[2] == Oper.OR:
        if idx == 0:
            val = ((v0 + 1) % 2) | v1
        else:
            val = v0 | ((v1 + 1) % 2)
    else:
        if idx == 0:
            val = ((v0 + 1) % 2) ^ v1
        else:
            val = v0 ^ ((v1 + 1) % 2)
    return val != orig_val

def get_outputs(o_gate:str, connections:list[Gate], vals:dict[str, int]) -> list[str]:
    inputs = []
    for gate in connections:
        if gate[3] == o_gate:
            if not(gate[0].startswith('x') or gate[0].startswith('y')):
                if swap_gate(gate, 0, vals, vals[o_gate]):
                    inputs.extend(get_outputs(gate[0], connections, vals))
                    inputs.append(gate[0])
            if not(gate[1].startswith('x') or gate[1].startswith('y')):
                if swap_gate(gate, 1, vals, vals[o_gate]):
                    inputs.extend(get_outputs(gate[1], connections, vals))
                    inputs.append(gate[1])
            break
    return inputs

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    connections_read = False
    connections = []
    init_vals = {}
    for line in mult_string:
        if connections_read:
            inputs = line.split()
            #print(inputs)
            connections.append(Gate((inputs[0], inputs[2], Oper.get_enum(inputs[1]), inputs[4])))
        elif not line:
            connections_read = True
        else:
            gate, val = line.split(':')
            val = int(val)
            init_vals[gate] = val
    
    main_part1(init_vals, connections)
    main_part2(connections)