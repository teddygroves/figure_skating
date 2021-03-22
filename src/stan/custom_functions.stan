/* This file is for your stan functions */

vector standardise_vector(vector v, real mu, real s){
    return (v - mu) / (2 * s);
}

matrix standardise_cols(matrix m, vector mu, vector s){
  matrix[rows(m), cols(m)] out;
  for (c in 1:cols(m))
    out[,c] = standardise_vector(m[,c], mu[c], s[c]);
  return out;
}

vector unstandardise_vector(vector v, real m, real s){
  return m + v * 2 * s;
}

vector col_means(matrix m){
  int C = cols(m);
  vector[C] out;
  for (c in 1:C)
    out[c] = mean(m[,c]);
  return out;
}

vector col_sds(matrix m){
  int C = cols(m);
  vector[C] out;
  for (c in 1:C)
    out[c] = sd(m[,c]);
  return out;
}

vector get_ordered_from_diffs(vector diffs, int fixed_ix, real fixed_val){
  /* Get an ordered vector of length K from a vector of K-1 differences, plus
     the index of an entry that is exactly fixed_val.
  */
  int K = rows(diffs) + 1;
  vector[K] out;
  out[fixed_ix] = fixed_val;
  out[1:fixed_ix-1] = reverse(-cumulative_sum(reverse(diffs[1:fixed_ix-1])));
  out[fixed_ix+1:K] = cumulative_sum(diffs[fixed_ix:K-1]);
  return out;
}
