# Step to test with a TDD spirit

- User run args:
    - img ref path (exist or not ...)
    - img ref loading (type supporting NPY, TIF,...)
    - user commands ? prepare,register,compare...
    - parameters checking...

- PREPARE section
    - test different shift values: just one on each axes (x, y or z), on both axes and on the three. Tests with negative and null values.
    - test the multiple input shifts option.
    - test the filling value

- REGISTER section
    - test registration on a simple img that are shifted with int
    - test if we have the same result calling a method directly or via registest wrapper
    - test multiple targets to register
    - test multiple methods to use
    - test multiple targets with multiple methods
    - if shifts.json exist

- COMPARE section
    - test if the outputs files are generated

## Development workflow

Find the basic way to use a feature
a. Write test for this feature
b. Develop feature
c. Document feature
iterate with more specific feature behavior
