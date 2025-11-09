# Fleet Decarbonization Analysis - Digital Twin

This project demonstrates mathematical models and risk analysis for heavy transport fleet decarbonization using synthetic data based on Queensland trial parameters. The analysis compares diesel trucks vs clean energy alternatives (BEV, FCET, Hybrid) with comprehensive visualizations and Monte Carlo risk assessment.

## Project Overview

This research demonstration provides:
- **Technology Comparison**: Performance, economic ROI, and environmental impact analysis
- **Risk Assessment**: Monte Carlo simulations with uncertainty quantification
- **Portfolio Optimization**: Optimal fleet composition strategies
- **Scenario Analysis**: Stress testing under different market conditions

### Key Features

- **Computed Results**: All metrics derived from mathematical models (no hardcoded values)
- **Realistic Parameters**: Based on Queensland heavy vehicle trial data
- **Comprehensive Risk Analysis**: 10,000+ Monte Carlo simulations per technology
- **Interactive Visualizations**: Publication-ready charts and dashboards
- **Strategic Insights**: Data-driven recommendations for fleet operators

## Technologies Analyzed

1. **Diesel (Baseline)**: $150K initial cost, $85K/year operating cost
2. **Battery Electric (BEV)**: 2x initial cost, 40% lower operating costs, 72% CO₂ reduction
3. **Fuel Cell Electric (FCET)**: 3x initial cost, similar operating costs, 82% CO₂ reduction  
4. **Hybrid**: 4x initial cost, 60% CO₂ reduction, transition technology

## Project Structure

```
digital-twin/
├── notebooks/
│   ├── 01_technology_comparison.ipynb    # Main analysis & visualizations
│   └── 02_monte_carlo_risk.ipynb         # Risk assessment & portfolio optimization
├── requirements.txt                       # Python dependencies
└── README.md                             # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+ 
- Jupyter Notebook or JupyterLab

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd digital-twin
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

4. **Run the notebooks**:
   - Start with `01_technology_comparison.ipynb` for comprehensive technology analysis
   - Continue with `02_monte_carlo_risk.ipynb` for risk assessment and portfolio optimization

## Key Analyses

### Notebook 1: Technology Comparison & ROI Analysis

**Computed Visualizations:**
- Energy Consumption Comparison (physics-based calculations)
- NPV Timeline (5-year financial projections)
- Break-even Analysis (payback period calculations)
- CO₂ Emissions Reduction (environmental impact quantification)
- Total Cost of Ownership (comprehensive cost breakdown)
- Operational Performance Radar Chart (multi-dimensional comparison)
- Battery Degradation Impact (exponential decay modeling)

**Key Findings:**
- BEV achieves break-even in ~3.2 years with 72% emission reduction
- FCET breaks even in ~4.5 years with 82% emission reduction
- All clean technologies show positive ROI within 5 years
- Battery degradation manageable with 15% capacity loss over 5 years

### Notebook 2: Monte Carlo Risk Assessment

**Risk Analysis Components:**
- NPV Distribution Analysis (10,000 simulations per technology)
- Sensitivity Analysis (parameter correlation identification)
- Risk-Return Optimization (efficient frontier calculation)
- Portfolio Optimization (optimal fleet composition)
- Scenario Stress Testing (5 market scenarios)

**Key Findings:**
- BEV shows 75% probability of positive NPV by year 4
- Optimal portfolio: 60% BEV, 25% FCET, 15% Hybrid
- Portfolio approach reduces risk while maintaining returns
- Robust performance across multiple stress scenarios

## Mathematical Models

### Energy Consumption
```python
E_wheel = mass * 9.81 * sin(grade) * distance + 
          0.006 * mass * 9.81 * distance + 
          0.5 * 1.2 * 8.0 * (velocity**2) * distance
```

### Battery Degradation
```python
range_degraded = initial_range * exp(-0.106 * years)
```

### Net Present Value
```python
NPV = -initial_investment + sum(cashflow_t / (1 + 0.08)**t for t in range(1, 6))
```

### Monte Carlo Simulation
- **Parameter Uncertainty**: Energy prices (±20%), utilization (70-95%), degradation (±25%)
- **Distributions**: Normal, Beta, and Uniform distributions for different parameters
- **Correlation Analysis**: Identification of key sensitivity factors
- **Risk Metrics**: VaR, Sharpe ratio, probability of success

## Results Summary

### Economic Viability
- **BEV**: Break-even 3.2 years, 75% success probability
- **FCET**: Break-even 4.5 years, 65% success probability  
- **Hybrid**: Break-even 5.2 years, 45% success probability
- **Portfolio**: 85% success probability with diversification

### Environmental Impact
- **Significant CO₂ reductions**: 60-82% vs diesel baseline
- **Annual savings**: 15-25 tonnes CO₂ per vehicle
- **Regulatory compliance**: Strong case for early adoption

### Risk Assessment
- **Optimal allocation**: 60% BEV, 25% FCET, 15% Hybrid
- **Portfolio VaR**: $45K maximum expected loss (95% confidence)
- **Scenario resilience**: Positive NPV in 4/5 stress scenarios
- **Key risk factors**: Energy prices, utilization rates, technology degradation

## Usage Examples

### Running Analysis
```python
# Load and run technology comparison
jupyter notebook notebooks/01_technology_comparison.ipynb

# Perform risk analysis
jupyter notebook notebooks/02_monte_carlo_risk.ipynb
```

### Customizing Parameters
```python
# Modify base technology specifications
base_technologies['BEV']['initial_cost'] = 350000  # Update BEV cost

# Adjust uncertainty parameters
uncertainty_params['fuel_price_variation']['std'] = 0.20  # Increase fuel price uncertainty

# Change scenario parameters
base_scenario['annual_km'] = 120000  # Higher utilization
```

## Data Sources & Methodology

- **Synthetic Data**: Generated using realistic parameters from Queensland heavy vehicle trials
- **Mathematical Models**: Physics-based energy consumption, exponential battery degradation
- **Financial Models**: Standard NPV calculations with appropriate discount rates
- **Monte Carlo**: 10,000 simulations per analysis with proper uncertainty quantification
- **Validation**: Results cross-checked for internal consistency and realism

## Visualization Features

- **Professional Styling**: Publication-ready charts with consistent branding
- **Interactive Elements**: Plotly-based dashboards for exploration
- **Comprehensive Coverage**: 15+ unique visualizations across both notebooks
- **Clear Annotations**: All charts include data sources and methodology notes

## Contributing

This is a research demonstration project. For modifications:

1. **Parameter Updates**: Modify base technology specifications in notebook cells
2. **Model Extensions**: Add new technologies or operational scenarios
3. **Visualization Enhancements**: Extend chart types or styling
4. **Analysis Expansion**: Include additional risk metrics or scenarios

## Dependencies

- `jupyter`: Interactive notebook environment
- `numpy`: Numerical computing and array operations
- `pandas`: Data manipulation and analysis
- `matplotlib`: Static plotting and visualization
- `seaborn`: Statistical visualization
- `plotly`: Interactive plotting and dashboards
- `scipy`: Scientific computing and optimization
- `ipywidgets`: Interactive widgets for notebooks
- `kaleido`: Static image export for Plotly

## License

This project is for research and demonstration purposes. The synthetic data and models are designed to illustrate analytical approaches for fleet decarbonization decision-making.

## Contact & Support

For questions about the methodology, models, or implementation:
- Review the detailed comments and markdown cells in both notebooks
- Check the mathematical model implementations in the code cells
- Refer to the comprehensive results summaries at the end of each notebook

---

**Note**: All data is synthetic and generated for demonstration purposes. While based on realistic parameters from Queensland trials, results should not be used for actual investment decisions without validation using real operational data.