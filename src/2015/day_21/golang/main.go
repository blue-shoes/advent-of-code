package main

import (
	"fmt"
	"math"
	"regexp"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

type Item struct {
	cost, damage, armor int
}

type Player struct {
	hp, attack, defense int
}

func combinations() [][]int {
	combos := make([][]bool, 8)
	for i := range 8 {
		combos[i] = []bool{i < 8, (i/4)%2 == 1, (i/2)%2 == 1, i%2 == 0}
	}
	intCombos := make([][]int, 8)
	for i := range 8 {
		intCombos[i] = make([]int, 4)
		for j := range 4 {
			if combos[i][j] {
				intCombos[i][j] = 1
			} else {
				intCombos[i][j] = 0
			}
		}
	}
	return intCombos
}

func mainPart1(weapons []Item, armor []Item, rings []Item, boss Player) {

	minGold := 100000
	for _, w := range weapons {
		for _, a := range armor {
			for r_i, r := range rings {
				for _, r2 := range rings[r_i+1:] {

					for _, combo := range combinations() {

						attack := w.damage*combo[0] + r.damage*combo[2] + r2.damage*combo[3]
						defense := a.armor*combo[1] + r.armor*combo[2] + r2.armor*combo[3]

						perTurnAttack := int(math.Max(float64(attack-boss.defense), 1))
						perTurnDamage := int(math.Max(float64(boss.attack-defense), 1))

						hitsBeforeDeath := 100 / perTurnDamage
						if 100%perTurnDamage != 0 {
							hitsBeforeDeath += 1
						}

						if perTurnAttack*hitsBeforeDeath >= boss.hp {
							gold := w.cost*combo[0] + a.cost*combo[1] + r.cost*combo[2] + r2.cost*combo[3]
							if gold < minGold {
								minGold = gold
							}
						}
					}

				}
			}
		}
	}

	fmt.Printf("Minimum gold to win is %d.\n", minGold)
}

func mainPart2(weapons []Item, armor []Item, rings []Item, boss Player) {

	maxGold := 0
	for _, w := range weapons {
		for _, a := range armor {
			for r_i, r := range rings {
				for _, r2 := range rings[r_i+1:] {
					if w.cost+a.cost+r.cost+r2.cost < maxGold {
						continue
					}
					for _, combo := range combinations() {

						attack := w.damage*combo[0] + r.damage*combo[2] + r2.damage*combo[3]
						defense := a.armor*combo[1] + r.armor*combo[2] + r2.armor*combo[3]

						perTurnAttack := int(math.Max(float64(attack-boss.defense), 1))
						perTurnDamage := int(math.Max(float64(boss.attack-defense), 1))

						hitsBeforeDeath := 100 / perTurnDamage
						if 100%perTurnDamage != 0 {
							hitsBeforeDeath += 1
						}

						if perTurnAttack*hitsBeforeDeath < boss.hp {
							gold := w.cost*combo[0] + a.cost*combo[1] + r.cost*combo[2] + r2.cost*combo[3]
							if gold > maxGold {
								maxGold = gold
							}
						}
					}
				}
			}
		}
	}

	fmt.Printf("Maximum gold to lose is %d.\n", maxGold)
}

func main() {
	shopLines := utility.ParseLines("../shop.txt")

	weaponsRead := false
	armorRead := false

	weapons := make([]Item, 0)
	armor := make([]Item, 0)
	rings := make([]Item, 0)

	r1 := regexp.MustCompile(`[^\+](\d+)`)

	for _, line := range shopLines {
		if strings.HasPrefix(line, "Weapons") {
			weaponsRead = true
			continue
		}
		if strings.HasPrefix(line, "Armor") {
			weaponsRead = false
			armorRead = true
			continue
		}
		if strings.HasPrefix(line, "Rings") {
			armorRead = false
			continue
		}
		if len(strings.TrimSpace(line)) == 0 {
			continue
		}

		match := utility.StringArrayToInts(r1.FindAllString(line, -1))

		item := Item{cost: match[0], damage: match[1], armor: match[2]}
		if weaponsRead {
			weapons = append(weapons, item)
		} else if armorRead {
			armor = append(armor, item)
		} else {
			rings = append(rings, item)
		}
	}

	bossLines := utility.ParseLines("../boss.txt")

	boss := Player{hp: utility.Atoi(r1.FindAllString(bossLines[0], 1)[0]), attack: utility.Atoi(r1.FindAllString(bossLines[1], 1)[0]), defense: utility.Atoi(r1.FindAllString(bossLines[2], 1)[0])}

	mainPart1(weapons, armor, rings, boss)
	mainPart2(weapons, armor, rings, boss)

}
