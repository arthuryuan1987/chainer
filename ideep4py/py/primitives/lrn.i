%{
    #define SWIG_FILE_WITH_INIT
    #include "lrn_py.h"
    #include "op_param.h"
%}

%include "param.i"
%include "std_vector.i"
%include "lrn_py.h"

%template(localResponseNormalization) LocalResponseNormalization_Py<float>;

//
// Python API for LocalResponseNormalization
//
// std::vector<mdarray*> LocalResponseNormalization_Py::Forward(
//                        mdarray *src,
//                        lrn_prarm_t *pp);
// mdarray* LocalResponseNormalization_Py::Backward(
//                        mdarray *src,
//                        mdarray *diff_dst,
//                        mdarray *ws,
//                        lrn_param_t *pp);
