// eslint-disable-next-line import/extensions
import validate from './validate.js';

const $emailInput = document.querySelector('.signup-form-email');
const $duplicateButton = document.querySelector('.signup-form-email-button');
const $signupButton = document.querySelector('.form-button');

const regEmail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;

document.querySelector('.signup-form').oninput = e => {
  if (e.target.matches('#name')) {
    validate.nameValidate(e.target.value, 0, $signupButton);
  } else if (e.target.matches('#email')) {
    validate.emailValidate(e.target.value, 1, $signupButton, false);

    $emailInput.querySelector('.icon-success').classList.add('hidden');
    $emailInput.querySelector('.icon-error').classList.remove('hidden');

    if (regEmail.test(e.target.value)) {
      $duplicateButton.removeAttribute('disabled');
    } else {
      $duplicateButton.setAttribute('disabled', '');
    }
  } else if (e.target.matches('#phone')) {
    validate.phoneValidate(e.target.value, 2, $signupButton);
  } else if (e.target.matches('#password')) {
    validate.passwordValidate(e.target.value, 3, $signupButton);
    validate.passwordConfirmValidate(
      e.target.value !== document.querySelector('#confirm-password').value,
      4,
      $signupButton
    );
  } else if (e.target.matches('#confirm-password')) {
    validate.passwordConfirmValidate(document.querySelector('#password').value !== e.target.value, 4, $signupButton);
  }
};

document.querySelector('.form-button').onclick = async e => {
  e.preventDefault();

  try {
    const { data: maxId } = await axios.get('/users');
    const newId = maxId.maxId;

    const len = document.querySelector('#password').value.length;

    await axios.post('/users/signup', {
      id: newId,
      name: document.querySelector('#name').value,
      email: document.querySelector('#email').value,
      phone: document.querySelector('#phone').value,
      password: document.querySelector('#password').value,
      passwordHint:
        document.querySelector('#password').value.slice(0, 2) +
        '*'.repeat(document.querySelector('#password').value.length - 2),
    });

    alert('회원가입이 완료되었습니다.');
    window.location.href = '/signin';
  } catch (error) {
    console.error(error);
  }
};

const $checkDuplicateMessage = document.querySelector('.signup-form-email .error');

const changeText = (message, color) => {
  $checkDuplicateMessage.innerHTML = message;
  $checkDuplicateMessage.style.color = color;
};

$duplicateButton.onclick = async () => {
  try {
    const emailValue = document.querySelector('#email').value;

    const res = await axios.get(`/users/email/${emailValue}`);
    const { isDuplicate } = res.data;

    if (isDuplicate) {
      changeText('이미 존재하는 이메일 입니다.', '#ed2553');
    } else {
      changeText('사용 가능한 이메일 입니다.', '#2196f3');
      $emailInput.querySelector('.icon-error').classList.add('hidden');
      $emailInput.querySelector('.icon-success').classList.remove('hidden');
      validate.emailValidate(emailValue, 1, $signupButton);
    }
  } catch (error) {
    console.error(error);
  }
};
