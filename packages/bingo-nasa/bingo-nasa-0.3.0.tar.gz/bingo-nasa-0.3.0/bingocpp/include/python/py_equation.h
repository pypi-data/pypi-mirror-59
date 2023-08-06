#ifndef BINGOCPP_INCLUDE_BINGOCPP_PY_EQUATION_H_
#define BINGOCPP_INCLUDE_BINGOCPP_PY_EQUATION_H_

#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include "BingoCpp/equation.h"

namespace bingo {

class PyEquation : public Equation {
 public:
  Eigen::ArrayXXd 
  EvaluateEquationAt(const Eigen::ArrayXXd &x) const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      Eigen::ArrayXXd,
      Equation,
      "evaluate_equation_at",
      EvaluateEquationAt,
      x
    );
  }

  EvalAndDerivative
  EvaluateEquationWithXGradientAt(const Eigen::ArrayXXd &x) const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      EvalAndDerivative,
      Equation,
      "evaluate_equation_with_x_gradient_at",
      EvaluateEquationWithXGradientAt,
      x
    );
  }

  EvalAndDerivative
  EvaluateEquationWithLocalOptGradientAt(const Eigen::ArrayXXd &x) const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      EvalAndDerivative,
      Equation,
      "evaluate_equation_with_local_opt_gradient_at",
      EvaluateEquationWithLocalOptGradientAt,
      x
    );
  }

  std::string GetLatexString() const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      std::string,
      Equation,
      "get_latex_string",
      GetLatexString,
    );
  }

  std::string GetConsoleString() const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      std::string,
      Equation,
      "get_console_string",
      GetConsoleString,
    );
  }

  std::string GetStackString() const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      std::string,
      Equation,
      "get_Stack_string",
      GetStackString,
    );
  }

  int GetComplexity() const override {
    PYBIND11_OVERLOAD_PURE_NAME(
      int,
      Equation,
      "get_complexity",
      GetComplexity,
    );
  }
};
} // namespace bingo
#endif // BINGOCPP_INCLUDE_BINGOCPP_PY_EQUATION_H_