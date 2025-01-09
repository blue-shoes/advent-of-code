package main

import (
	"container/heap"
	"fmt"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

type Spell struct {
	name                                        string
	mana, damage, heal, armor, turns, replenish int
}

func processSpell(spell Spell, timer map[Spell]int, hp, mana, bossHp int) (int, int, int) {
	fmt.Println(spell, timer)
	for k, v := range timer {
		if v > 0 {
			bossHp -= k.damage
			mana += k.replenish
			timer[k] = v - 1
		}
	}
	hp += spell.heal
	if spell.turns == 0 {
		bossHp -= spell.damage
	}
	mana -= spell.mana
	if spell.turns > 0 {
		timer[spell] = spell.turns
	}

	return hp, mana, bossHp
}

func processAttack(timer map[Spell]int, hp, bossHp, bossAttack, mana int) (int, int, int) {
	defense := 0
	for k, v := range timer {
		if v > 0 {
			bossHp -= k.damage
			mana += k.replenish
			defense += k.armor
			timer[k] = v - 1
		}
	}
	if bossHp <= 0 {
		return hp, bossHp, mana
	}

	hp = hp - bossAttack + defense

	return hp, bossHp, mana

}

func evaluateMove(startItem *utility.Item, spell *Spell, hardMode bool) (*utility.Item, bool, bool) {
	sItem := *startItem

	le := sItem.Value.([][]int)
	lastEvolution := make([][]int, len(le))
	copy(lastEvolution, le)
	size := len(lastEvolution)

	var newHp, newBossHp, newMana, newSpentMana, pT, sT, rT int
	var evolution [][]int

	if size > 0 {
		lastState := lastEvolution[size-1]

		newHp = lastState[0]
		newBossHp = lastState[1]
		newMana = lastState[2]
		newSpentMana = lastState[7]

		pT = lastState[4]
		sT = lastState[5]
		rT = lastState[6]
	} else {
		newHp = 50
		newBossHp = bossHp
		newMana = 500
		newSpentMana = 0

		pT = 0
		sT = 0
		rT = 0
	}

	if hardMode {
		newHp -= 1
	}

	if newHp <= 0 {
		return &utility.Item{Priority: -1000000}, true, false
	}

	if pT > 0 {
		newBossHp -= 3
	}
	if rT > 0 {
		newMana += 101
	}

	pT--
	sT--
	rT--

	if newBossHp <= 0 {
		//Winner
		nextMove := []int{newHp, newBossHp, newMana, 0, pT, sT, rT, newSpentMana}
		evolution = append(lastEvolution, nextMove)
		return &utility.Item{Value: evolution, Priority: newSpentMana}, false, true
	}

	if spell.mana > newMana {
		//Cant do spell
		return &utility.Item{Priority: -1000000}, true, false
	}

	if spell.turns > 0 {
		if (spell.name == "Poison" && pT > 0) || (spell.name == "Shield" && sT > 0) || (spell.name == "Recharge" && rT > 0) {
			return &utility.Item{Priority: -1000000}, true, false
		}
		if spell.name == "Poison" {
			pT = spell.turns
		} else if spell.name == "Shield" {
			sT = spell.turns
		} else {
			rT = spell.turns
		}
	} else {
		newHp += spell.heal
		newBossHp -= spell.damage
	}
	newMana -= spell.mana
	newSpentMana += spell.mana

	if newBossHp <= 0 {
		//Winner
		nextMove := []int{newHp, newBossHp, newMana, 0, pT, sT, rT, newSpentMana}
		evolution = append(lastEvolution, nextMove)
		return &utility.Item{Value: evolution, Priority: newSpentMana}, false, true
	}

	armor := 0

	if pT > 0 {
		newBossHp -= 3
	}
	if rT > 0 {
		newMana += 101
	}
	if sT > 0 {
		armor = 7
	}

	pT--
	sT--
	rT--

	if newBossHp <= 0 {
		//Winner
		nextMove := []int{newHp, newBossHp, newMana, 0, pT, sT, rT, newSpentMana}
		evolution = append(lastEvolution, nextMove)
		return &utility.Item{Value: evolution, Priority: newSpentMana}, false, true
	}

	newHp -= (bossAttack - armor)
	nextMove := []int{newHp, newBossHp, newMana, armor, pT, sT, rT, newSpentMana}
	evolution = append(lastEvolution, nextMove)

	item := utility.Item{Value: evolution, Priority: newSpentMana}
	return &item, newHp <= 0, false
}

func mainPart(spells []Spell, hardMode bool) {
	nq := &utility.PriorityQueue{}
	heap.Init(nq)
	var best [][]int
	var lowestMana int
	heap.Push(nq, &utility.Item{Value: make([][]int, 0), Priority: 0})
	for {
		if nq.Len() == 0 {
			// There's no combos left, return found false.
			fmt.Println("No combos found")
			return
		}
		current := heap.Pop(nq).(*utility.Item)
		size := len(current.Value.([][]int))
		if size > 0 && current.Value.([][]int)[size-1][1] <= 0 {
			// Beat boss.
			best = current.Value.([][]int)
			lowestMana = current.Priority
			break
		}

		for _, spell := range spells {
			nextMove, fail, _ := evaluateMove(current, &spell, hardMode)
			if fail {
				continue
			}
			heap.Push(nq, nextMove)
		}
	}

	fmt.Printf("Won using %d mana.\n", lowestMana)
	fmt.Println("Game was:")
	for _, move := range best {
		fmt.Println(move)
	}
}

var bossHp int
var bossAttack int

func main() {

	spellLines := utility.ParseLines("../spells.txt")

	spells := make([]Spell, 0)
	for _, line := range spellLines {
		split := strings.Split(line, " ")
		s := utility.StringArrayToInts(split[1:])
		spells = append(spells, Spell{name: split[0], mana: s[0], damage: s[1], heal: s[2], armor: s[3], turns: s[4], replenish: s[5]})
	}

	bossLines := utility.ParseLines("../boss.txt")
	bossHp = utility.Atoi(strings.Split(bossLines[0], " ")[2])
	//bossHp = 14
	bossAttack = utility.Atoi(strings.Split(bossLines[1], " ")[1])
	//bossAttack = 8

	mainPart(spells, false)
	mainPart(spells, true)
}
