import AugmentedMatrixForm from "./AugmentedMatrixForm";

// Maps a solver's input_schema.type to the form component that collects its input.
// A new kind of method (e.g. "square_matrix") only needs an entry here.
export const inputForms = {
  augmented_matrix: AugmentedMatrixForm,
};
