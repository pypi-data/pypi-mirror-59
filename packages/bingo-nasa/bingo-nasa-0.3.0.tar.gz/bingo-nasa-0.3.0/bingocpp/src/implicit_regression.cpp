#include <Eigen/Dense>
#include <Eigen/Core>

#include "BingoCpp/implicit_regression.h"

namespace bingo {

ImplicitTrainingData *ImplicitTrainingData::GetItem(int item) {
  return new ImplicitTrainingData(x.row(item), dx_dt.row(item));
}

ImplicitTrainingData *ImplicitTrainingData::GetItem(
    const std::vector<int> &items) {
  Eigen::ArrayXXd temp_in(items.size(), x.cols());
  Eigen::ArrayXXd temp_out(items.size(), dx_dt.cols());

  for (std::size_t row = 0; row < items.size(); row ++) {
    temp_in.row(row) = x.row(items[row]);
    temp_out.row(row) = dx_dt.row(items[row]);
  }
  return new ImplicitTrainingData(temp_in, temp_out);
}

void normalize_by_row(Eigen::ArrayXXd *data_array);
Eigen::ArrayXXd dfdx_dot_dfdt(bool normalize_dot,
                              const Eigen::ArrayXXd &dx_dt,
                              const Eigen::ArrayXXd &grad);
bool not_enough_parameters_used(int required_params, 
                                const Eigen::ArrayXXd &dot_product);

Eigen::ArrayXXd ImplicitRegression::EvaluateFitnessVector(
    const Equation &individual) const {
  EvalAndDerivative eval_and_grad 
      = individual.EvaluateEquationWithXGradientAt(
      ((ImplicitTrainingData*)training_data_)->x);
  Eigen::ArrayXXd dot_product = dfdx_dot_dfdt(
      normalize_dot_,
      ((ImplicitTrainingData*)training_data_)->dx_dt,
      eval_and_grad.second);

  if (required_params_ != kNoneRequired
      && not_enough_parameters_used(required_params_, dot_product)) {
    return Eigen::ArrayXd::Constant(
        ((ImplicitTrainingData*)training_data_)->x.rows(),
         std::numeric_limits<double>::infinity());
  }
  // NOTE tylertownsend: may need to verify eigen NaN conditions
  Eigen::ArrayXXd denominator = dot_product.abs().rowwise().sum();
  Eigen::ArrayXXd normalized_fitness = 
      dot_product.rowwise().sum() / denominator;
  return normalized_fitness.unaryExpr([](double v) { 
    return std::isfinite(v) ? v : std::numeric_limits<double>::infinity();
  });
}

void normalize_by_row(Eigen::ArrayXXd *data_array) {
  Eigen::ArrayXXd norm_array = data_array->rowwise().norm();
  for (int i = 0; i < norm_array.rows(); i ++) {
    data_array->row(i) /= norm_array.row(i)[0];
  }
}

Eigen::ArrayXXd dfdx_dot_dfdt(bool normalize_dot,
                              const Eigen::ArrayXXd &dx_dt,
                              const Eigen::ArrayXXd &grad) {
  Eigen::ArrayXXd left_dot = grad;
  Eigen::ArrayXXd right_dot = dx_dt;
  if (normalize_dot) {
    normalize_by_row(&left_dot);
    normalize_by_row(&right_dot);
  }

  return left_dot * right_dot;
}

bool not_enough_parameters_used(int required_params, 
                                const Eigen::ArrayXXd &dot_product) {
  auto num_params_used = (dot_product.abs() > 1e-16).rowwise().count();
  return !(num_params_used >= required_params).any();
}
} // namespace bingo