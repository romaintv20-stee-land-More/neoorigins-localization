#!/usr/bin/env python3
"""Temporary finalizer for the four Kabyle labels the generic 1.3B pass cannot resolve."""
import repair_kabyle_13b_shards as repair

repair.MANUAL_REPAIRS.update({
    "Necromancer Slow Regen": "Necromancer: ales n tmeddurt aẓayan",
    "Draconic Attack Bonus": "Draconic: abaɣur n uẓdam",
    "Sculkborn Sonic Bolt": "Sculkborn: aẓdam n ṣṣut",
    "Web Walker": "Tikli ɣef uẓeṭṭa",
})

if __name__ == "__main__":
    repair.main()
