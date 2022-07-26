const form = document.getElementById('form');
const faci = document.getElementById('facility');
const setError = (element, message) => {
    
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const validateInputs = () => {
    const usernameValue = faci.value.trim();


    if(usernameValue === '') {
        setError(faci, 'Facility is required');
    } else {
        setSuccess(faci);
    }

};
