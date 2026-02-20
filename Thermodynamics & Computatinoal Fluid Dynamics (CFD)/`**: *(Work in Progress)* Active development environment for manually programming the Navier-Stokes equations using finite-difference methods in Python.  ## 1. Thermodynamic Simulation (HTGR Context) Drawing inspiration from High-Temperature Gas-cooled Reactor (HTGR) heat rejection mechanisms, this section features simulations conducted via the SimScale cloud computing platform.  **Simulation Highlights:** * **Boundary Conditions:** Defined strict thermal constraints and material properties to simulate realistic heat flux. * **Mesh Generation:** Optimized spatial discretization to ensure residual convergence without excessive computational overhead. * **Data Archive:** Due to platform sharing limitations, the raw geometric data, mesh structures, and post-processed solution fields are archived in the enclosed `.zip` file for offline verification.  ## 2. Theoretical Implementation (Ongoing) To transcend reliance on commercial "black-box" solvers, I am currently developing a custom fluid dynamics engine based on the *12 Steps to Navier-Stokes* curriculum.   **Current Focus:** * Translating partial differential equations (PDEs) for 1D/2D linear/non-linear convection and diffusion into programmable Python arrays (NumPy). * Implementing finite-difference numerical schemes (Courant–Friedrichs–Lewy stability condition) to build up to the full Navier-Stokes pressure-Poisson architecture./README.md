# 🌪️ Thermodynamics & Computational Fluid Dynamics (CFD)

This module encapsulates my computational modeling of thermal dynamics and fluid mechanics, bridging commercial solver execution with independent numerical method programming.

## 📂 Repository Structure

* **`SimScale_Thermal_Results.zip`**: Complete archive of solution fields, boundary condition configurations, and thermal flux reports. 
* **`simulation_preview.png`**: Visual extraction of the thermodynamic temperature gradients and mesh convergence.
* **`Navier_Stokes_Implementation/`**: *(Work in Progress)* Active development environment for manually programming the Navier-Stokes equations using finite-difference methods in Python.

## 1. Thermodynamic Simulation (HTGR Context)
Drawing inspiration from High-Temperature Gas-cooled Reactor (HTGR) heat rejection mechanisms, this section features simulations conducted via the SimScale cloud computing platform.

**Simulation Highlights:**
* **Boundary Conditions:** Defined strict thermal constraints and material properties to simulate realistic heat flux.
* **Mesh Generation:** Optimized spatial discretization to ensure residual convergence without excessive computational overhead.
* **Data Archive:** Due to platform sharing limitations, the raw geometric data, mesh structures, and post-processed solution fields are archived in the enclosed `.zip` file for offline verification.

## 2. Theoretical Implementation (Ongoing)
To transcend reliance on commercial "black-box" solvers, I am currently developing a custom fluid dynamics engine based on the *12 Steps to Navier-Stokes* curriculum. 

**Current Focus:**
* Translating partial differential equations (PDEs) for 1D/2D linear/non-linear convection and diffusion into programmable Python arrays (NumPy).
* Implementing finite-difference numerical schemes (Courant–Friedrichs–Lewy stability condition) to build up to the full Navier-Stokes pressure-Poisson architecture.