/* The simplest figure skating scores model I could think of*/
functions {
#include custom_functions.stan
}
data {
  int<lower=1> N;
  int<lower=1> N_skater;
  int<lower=1> N_grade;
  int<lower=1,upper=N_skater> skater[N];
  int<lower=1,upper=N_grade> y[N];
  int<lower=1> N_test;
  int<lower=1,upper=N_skater> skater_test[N_test];
  int<lower=1,upper=N_grade> y_test[N_test];
  int<lower=0,upper=1> likelihood;
  vector[2] prior_mu;
  vector[2] prior_cutpoint_diffs;
}
parameters {
  real mu;
  vector[N_skater] ability;
  vector<lower=0>[N_grade-2] cutpoint_diffs;
}
transformed parameters {
  ordered[N_grade-1] cutpoints = get_ordered_from_diffs(cutpoint_diffs, 5, 0);
}
model {
  mu ~ normal(prior_mu[1], prior_mu[2]);
  ability ~ normal(0, 1);
  cutpoint_diffs ~ normal(prior_cutpoint_diffs[1], prior_cutpoint_diffs[2]);
  if (likelihood){
    y ~ ordered_logistic(mu + ability[skater], cutpoints);
  }
}
generated quantities {
  int yrep[N_test];
  vector[N_test] llik;
  for (n in 1:N_test){
    real eta = mu + ability[skater_test[n]];
    yrep[n] = ordered_logistic_rng(eta, cutpoints);
    llik[n] = ordered_logistic_lpmf(y_test[n] | eta, cutpoints);
  }
}
