#define BOOST_TEST_MODULE epg_Regular
#include <boost/test/unit_test.hpp>

#include "sycomore/epg/Regular.h"
#include "sycomore/Species.h"
#include "sycomore/units.h"

#define TEST_COMPLEX_EQUAL(v1, v2) \
    { \
        sycomore::Complex const c1(v1), c2(v2); \
        BOOST_TEST(c1.real() == c2.real()); \
        BOOST_TEST(c1.imag() == c2.imag()); \
    }

void test_model(
    sycomore::epg::Regular const & model,
    std::vector<std::vector<sycomore::Complex>> const & expected_states)
{
    
    auto const & states = model.states();
    BOOST_TEST(model.states_count() == expected_states.size());
    BOOST_TEST(states.size() == 3*expected_states.size());
    
    for(std::size_t i=0; i<model.states_count(); ++i)
    {
        auto && expected_state = expected_states[i];
        auto && state = model.state(i);
        
        BOOST_TEST(state.size() == expected_state.size());
        for(std::size_t j=0; j<state.size(); ++j)
        {
            TEST_COMPLEX_EQUAL(states[3*i+j], expected_state[j]);
            TEST_COMPLEX_EQUAL(state[j], expected_state[j]);
        }
    }
    BOOST_TEST(model.echo() == expected_states[0][0]);
}

BOOST_AUTO_TEST_CASE(Empty)
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms);
        
    sycomore::epg::Regular model(species);
    
    test_model(model, {{0,0,1}});
}

BOOST_AUTO_TEST_CASE(Pulse, *boost::unit_test::tolerance(1e-9))
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms, 3*um*um/ms);
        
    sycomore::epg::Regular model(species);
    model.apply_pulse(47*deg, 23*deg);
    
    test_model(
        model, 
        {
            {
                {0.2857626571584661, -0.6732146319308543},
                {0.2857626571584661, +0.6732146319308543},
                0.6819983600624985}});
}

BOOST_AUTO_TEST_CASE(Gradient, *boost::unit_test::tolerance(1e-9))
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms, 3*um*um/ms);
        
    sycomore::epg::Regular model(species);
    model.apply_pulse(47*deg, 23*deg);
    model.shift();
    
    test_model(
        model, 
        {
            {0, 0, 0.6819983600624985},
            {{0.2857626571584661, -0.6732146319308543}, 0, 0}});
}

BOOST_AUTO_TEST_CASE(Relaxation, *boost::unit_test::tolerance(1e-9))
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms, 3*um*um/ms);
        
    sycomore::epg::Regular model(species);
    model.apply_pulse(47*deg, 23*deg);
    model.shift();
    model.relaxation(10*ms);
    
    test_model(
        model, 
        {
            {0, 0, 0.6851625292479138},
            {{0.2585687448743616, -0.6091497893403431}, 0, 0}});
}

BOOST_AUTO_TEST_CASE(Diffusion, *boost::unit_test::tolerance(1e-9))
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms, 3*um*um/ms);
        
    sycomore::epg::Regular model(species);
    model.apply_pulse(47*deg, 23*deg);
    model.shift();
    model.relaxation(10*ms);
    model.diffusion(10*ms, 2*mT/m);
    
    test_model(
        model, 
        {
            {0, 0, 0.6851625292479138},
            {{0.25805111586158685, -0.6079303318059787}, 0, 0}});
}

BOOST_AUTO_TEST_CASE(TimeInterval, *boost::unit_test::tolerance(1e-9))
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms, 3*um*um/ms);
        
    sycomore::epg::Regular model(species);
    model.apply_pulse(47*deg, 23*deg);
    model.apply_time_interval(10*ms, 2*mT/m);
    
    test_model(
        model, 
        {
            {0, 0, 0.6851625292479138},
            {{0.2584947343504123, -0.6089754314724013}, 0, 0}});
}

BOOST_AUTO_TEST_CASE(UnitGradient, *boost::unit_test::tolerance(1e-9))
{
    using namespace sycomore::units;
    sycomore::Species const species(1000*ms, 100*ms);
        
    sycomore::epg::Regular model(species, {0,0,1}, 100, 10*mT/m*ms);
    model.apply_pulse(47*deg, 23*deg);
    
    /* First time interval: 1*unit gradient area */
    model.apply_time_interval(10*ms, 1*mT/m);
    
    test_model(
        model, 
        {
            {0, 0, 0.6851625292479138},
            {{0.2585687448743616, -0.609149789340343}, 0, 0}});
    
    /* Second time interval: 2*unit gradient area */
    model.apply_time_interval(10*ms, 2*mT/m);
    test_model(
        model, 
        {
            {0, 0, 0.6882952144238884},
            {0, 0, 0},
            {0, 0, 0},
            {{0.2339626754969161, -0.5511815225838647}, 0, 0}});
    
    /* Third time interval: -3*unit gradient area */
    model.apply_time_interval(10*ms, -3*mT/m);
    test_model(
        model, 
        {
            {
                {0.2116981832134146, -0.49872966576391303}, 
                {0.2116981832134146, +0.49872966576391303}, 
                0.6913967288615507},
            {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}});
    
    BOOST_CHECK_THROW(
        model.apply_time_interval(12*ms, 2*mT/m), std::runtime_error);
}
