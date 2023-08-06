#pragma once

namespace conmech
{
namespace stiffness_checker
{

class StiffnessParm
{
 public:
  StiffnessParm(){}

  ~StiffnessParm(){};

 public:
  double getShearModulus(const double& E, const double& poisson_ratio) { return 0.5 * E / (1 + poisson_ratio); }
  double getPoissonRatio(const double& E, const double& G) { return (E / (2.0*G) - 1); }

  /**
   * material density, unit: kN/m^3
   */
  double density_;

  /**
   * unit: kN/m^2
   */
  double youngs_modulus_;

  /**
   * unit: kN/m^2
   */
  double shear_modulus_;

  /**
   * unit: kN/m^2
   */
  double tensile_yeild_stress_;

  /**
   * unit: [] (unitless)
   * G = E / 2(1+mu),
   * where G is shear modulus, E is Young's modulus
   * mu is poission ratio
   */
  double poisson_ratio_;

  // TODO: this radius should be associated with geometry
  /**
   * raidus of the cross section
   * unit: meter
   */
  // double radius_;
  double cross_sec_area_;

  // torsion constant (around local x axis)
  // for solid circle: (1/2)pi*r^4, unit: m^4
  // see: https://en.wikipedia.org/wiki/Torsion_constant#Circle
  double Jx_;

  // area moment of inertia (bending about local y,z-axis)
  // assuming solid circular area of radius r, unit: m^4
  // see: https://en.wikipedia.org/wiki/List_of_area_moments_of_inertia
  // note this is slender rod of length L and Mass M, spinning around end
  double Iy_;
  double Iz_;
};

} // ns stiffness_checker
} // ns conmech
