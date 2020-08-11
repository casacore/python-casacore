#include <iostream>

#include <boost/function.hpp>
#include <boost/function_types/components.hpp>
#include <boost/function_types/function_type.hpp>
#include <boost/function_types/result_type.hpp>
#include <boost/python.hpp>
#include <boost/tuple/tuple.hpp>

namespace details {

/// @brief Functor that will invoke a function while holding a guard.
///        Upon returning from the function, the guard is released.
template <typename Signature,
          typename Guard>
class guarded_function
{
public:

  typedef typename boost::function_types::result_type<Signature>::type
      result_type;

  template <typename Fn>
  guarded_function(Fn fn)
    : fn_(fn)
  {}

  template <typename... Args>
  result_type operator()(Args... args)
  {
    Guard g;
    return fn_(args...);
  } 

private:
  boost::function<Signature> fn_;
};

/// @brief Provides signature type.
template <typename Signature>
struct mpl_signature
{
  typedef typename boost::function_types::components<Signature>::type type;
};

// Support boost::function.
template <typename Signature>
struct mpl_signature<boost::function<Signature> >:
  public mpl_signature<Signature>
{};

/// @brief Create a callable object with guards.
template <typename Guard,
          typename Fn,
          typename Policy>
boost::python::object with_aux(Fn fn, const Policy& policy)
{
  // Obtain the components of the Fn.  This will decompose non-member
  // and member functions into an mpl sequence.
  //   R (*)(A1)    => R, A1
  //   R (C::*)(A1) => R, C*, A1
  typedef typename mpl_signature<Fn>::type mpl_signature_type;

  // Synthesize the components into a function type.  This process
  // causes member functions to require the instance argument.
  // This is necessary because member functions will be explicitly
  // provided the 'self' argument.
  //   R, A1     => R (*)(A1)
  //   R, C*, A1 => R (*)(C*, A1)
  typedef typename boost::function_types::function_type<
      mpl_signature_type>::type signature_type;

  // Create a callable boost::python::object that delegates to the
  // guarded_function.
  return boost::python::make_function(
    guarded_function<signature_type, Guard>(fn),
    policy, mpl_signature_type());
}

} // namespace details

/// @brief Create a callable object with guards.
template <typename Guard,
          typename Fn,
          typename Policy>
boost::python::object with(const Fn& fn, const Policy& policy)
{
  return details::with_aux<Guard>(fn, policy);
}

/// @brief Create a callable object with guards.
template <typename Guard,
          typename Fn>
boost::python::object with(const Fn& fn)
{
  return with<Guard>(fn, boost::python::default_call_policies());
}

/// @brief Guard that will unlock the GIL upon construction, and
///        reacquire it upon destruction.
struct no_gil
{
public:
  no_gil()  { state_ = PyEval_SaveThread(); }
  ~no_gil() { PyEval_RestoreThread(state_); }
private:
  PyThreadState* state_;
};

/// @brief Guard that prints to std::cout.
struct echo_guard 
{
  echo_guard()  { std::cout << "echo_guard()" << std::endl;  }
  ~echo_guard() { std::cout << "~echo_guard()" << std::endl; }
};
