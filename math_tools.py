def mod_power(x, m, n):
    if m == 0: return 1
    elif m == 1: return (x % n)
    else:
        current_val = 1
        current_x_powered = x
        power = 1
        cur_power = 1
        while(m > 1):
            if(m % 2 == 1):
                current_val = (current_val * current_x_powered) % n
                current_x_powered = (current_x_powered ** 2) % n
                m = (m-1)//2
            else:
                current_x_powered = (current_x_powered ** 2) % n
                m = m//2
        current_val = (current_val * current_x_powered) % n
        return(current_val)

# Asumsi x = 1 (mod n). Gunakan extended euclid untuk dapatkan a, b sehingga 
# ax + bn = 1
def inverse_modulo(x, n):
    old_r, r = x, n
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quo = old_r // r
        old_r, r = r, old_r - quo * r
        old_s, s = s, old_s - quo * s
        old_t, t = t, old_t - quo * t
    
    if old_s < 0:
        return old_s + n
    else: return old_s

def fpb(a, b):
    if(b==0): return a
    else: return fpb(b, a % b)
