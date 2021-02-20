import numpy as np

# 0.43846153846153846 modifier for resistance and defense
# level 90 Diluc, level 100 enemy 10% resistance
# base attack 311


def damage(atk, em, crit_rate, crit_dmg):
    # CW 4 stacks, a4, pyro goblet 1.031 --> multi 2.031

    # 'Q' 'A' 'E' A A 'E' 'A' A 'E' 'A' A A 'A'
    # level 8 talents
    # vape: Q + DoT + 3*N1 + N4 + E1 + E2 + E3
    # 3.264 + 0.96 + 3*1.5332 + 2.2903 + 1.5104 + 1.5616 + 2.0608 = 16.2467
    vape = 16.2467 * atk * 2.031 * 1.5 * (1 + (2.78 * em / (em + 1400)) + 0.15) * 0.43846153846153846
    # non vape: 2*DoT + N1 + 3*N2 + N3
    # 2*0.96 + 1.5332 + 3*1.4979 + 1.689 = 9.6359
    non_vape = 9.6359 * atk * 2.031 * 0.43846153846153846

    return (vape + non_vape) * (1 + min(crit_rate, 1) * crit_dmg)


def generate_rolls(rolls):
    # doesn't generate max rolls into a single stat except for the fourth
    # but that won't be optimal so whatever
    res = []
    for x in range(rolls):
        for y in range(rolls - x):
            for z in range(rolls - x - y):
                res.append(np.array([x, y, z, rolls - x - y - z]))
    return res


def calc(weapon_atk, weapon_secondary, artifact_main_stats, base_rolls):
    '''
    weapon_atk: weapon base attack
    weapon_secondary: 4 length np array [atk%, em, crit rate, crit damage]
    '''
    base_attack = 311 + weapon_atk
    sub_values = np.array([0.053, 23, 0.039, 0.078])  # atk, em, crit rate, crit damage

    base_subs = sub_values * base_rolls

    stats = np.array([1, 0, 0.242, 0.5]) + weapon_secondary + artifact_main_stats
    results = []
    for roll in generate_rolls(25):
        subs = sub_values * roll
        new_stats = stats + subs + base_subs
        new_stats[0] = new_stats[0] * base_attack + 311  # add feather
        dmg = damage(*new_stats)
        results.append((dmg, roll + base_rolls, new_stats))
    return results


# wgs r1 atk sands
# res = calc(607, np.array([0.696, 0, 0, 0]), np.array([0.466, 0, 0.312, 0]), np.array([4, 5, 4, 5]))
# top = sorted(res, key=lambda x: x[0], reverse=True)[0:100]
# print('WGS R1 atk sands')
# print('\n'.join(str(i) for i in top))


# wgs r1 em sands
# res = calc(607, np.array([0.696, 0, 0, 0]), np.array([0, 197, 0.312, 0]), np.array([5, 4, 4, 5]))
# top = sorted(res, key=lambda x: x[0], reverse=True)[0:100]
# print('WGS R1 em sands')
# rint('\n'.join(str(i) for i in top))


# # wgs r1 atk sands 25% uptime
res = calc(607, np.array([0.796, 0, 0, 0]), np.array([0.466, 0, 0.312, 0]), np.array([4, 5, 4, 5]))
top = sorted(res, key=lambda x: x[0], reverse=True)[0:100]
# print('WGS R1 atk sands 25% uptime')
# print('\n'.join(str(i) for i in top))

# # wgs r1 em sands 25% uptime
# res = calc(607, np.array([0.796, 0, 0, 0]), np.array([0, 197, 0.312, 0]), np.array([5, 4, 4, 5]))
# top = sorted(res, key=lambda x: x[0], reverse=True)[0:100]
# print('WGS R1 em sands 25% uptime')
# print('\n'.join(str(i) for i in top))

# # skyward pride no passive atk sands
# res = calc(674, np.array([0, 0, 0, 0]), np.array([0.466, 0, 0.312, 0]), np.array([4, 5, 4, 5]))
# top = sorted(res, key=lambda x: x[0], reverse=True)[0:15]
# print('skyward pride no passive')
# print('\n'.join(str(i) for i in top))

temp = []
for dmg, rolls, stats in top:
    rolls = ','.join(f'{i}' for i in rolls)
    stats = ','.join(f'{i:.2f}' for i in stats)
    temp.append(f'{dmg:.2f},{rolls},{stats}')
with open('results.csv', 'w') as f:
    f.write('damage,atk%,em,crit%,critdmg,atk,em,crit%,critdmg\n')
    f.writelines(f'{i}\n' for i in temp)
