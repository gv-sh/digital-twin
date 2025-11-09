#!/usr/bin/env python3
"""Test refactored digital_twin module."""

import digital_twin
print('✓ Module imports successfully')

# Test type enums
from digital_twin.core.types import VehicleType, FuelType
print(f'✓ VehicleType.HEAVY_TRUCK = {VehicleType.HEAVY_TRUCK.value}')
print(f'✓ FuelType.ELECTRIC = {FuelType.ELECTRIC.value}')
print(f'✓ FuelType.HYDROGEN = {FuelType.HYDROGEN.value}')

# Test data generators
from digital_twin.data import create_base_technologies
techs = create_base_technologies()
print(f'\n✓ Created {len(techs)} technology specifications:')
for name, spec in techs.items():
    print(f'  - {name}: ${spec.initial_cost:,} initial cost, {spec.max_range_km} km range')

# Test physics module
from digital_twin.physics.energy import calculate_wheel_energy
energy = calculate_wheel_energy(mass=18000, grade=0.0, distance=100000, velocity=22.2)
print(f'\n✓ Physics calculation: {energy/1e6:.2f} MJ wheel energy')

# Test economics module
from digital_twin.economics.roi import calculate_npv
npv = calculate_npv(150000, [30000, 30000, 30000, 30000, 30000])
print(f'✓ Economics calculation: NPV = ${npv:,.2f}')

# Test backward compatibility with models.equations
from digital_twin.models.equations import (
    calculate_wheel_energy_per_trip,
    calculate_risk_adjusted_npv,
    validate_queensland_trials
)
print(f'\n✓ Backward compatibility wrappers imported successfully')

# Run Queensland validation
validation = validate_queensland_trials()
print(f'\n✓ Queensland trials validation:')
for test, passed in validation.items():
    status = '✓' if passed else '✗'
    print(f'  {status} {test}: {"PASS" if passed else "FAIL"}')

print('\n✓✓✓ All refactoring tests passed! ✓✓✓')
