// eslint-disable-next-line import/extensions
import validate from './validate.js';

const $formButton = document.querySelector('.form-button');
const $findPassword = document.querySelector('.find-password');
const $deleteButton = document.querySelector('.delete-button');

document.querySelector('.signin-form').oninput = e => {
  if (e.target.matches('#email')) {
    validate.emailValidate(e.target.value, 0, $formButton);
  } else if (e.target.matches('#password')) {
    validate.passwordValidate(e.target.value, 1, $formButton);
  }
};

let checked = false;
document.querySelector('#auto__login').onchange = () => {
  checked = !checked;
};

$formButton.onclick = async e => {
  e.preventDefault();

  try {
    const { data: user } = await axios.post('/signin', {
      email: document.querySelector('#email').value,
      password: document.querySelector('#password').value,
      autoLogin: checked,
    });

    if (user) window.location.href = '/mypage';
  } catch (error) {
    document.querySelector('.singin-error-login').innerHTML = '아이디 또는 비밀번호가 잘못 입력 되었습니다.';
    console.error(error);
  }
};

const $modal = document.querySelector('.popup');

const popupHandle = () => {
  document.querySelector('.cover').classList.toggle('hidden');
  $modal.classList.toggle('hidden');
  $modal.querySelector('.error').textContent = '';
  $findPassword.value = '';
  $deleteButton.setAttribute('disabled', '');
};

document.querySelector('.find').onclick = e => {
  e.preventDefault();
  popupHandle();
};

$modal.querySelector('.cancle-button').onclick = () => {
  popupHandle();
};

document.querySelector('.signin-form-more').onclick = e => {
  if (!e.target.matches('a')) return;

  window.location.href = '/signup';
};

const regEmail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;
$findPassword.oninput = e => {
  if (regEmail.test(e.target.value)) {
    $deleteButton.removeAttribute('disabled');
  } else {
    $deleteButton.setAttribute('disabled', '');
  }
};

const checkPassword = async () => {
  try {
    const findPassword = $findPassword.value;
    const res = await axios.get(`/user/find/${findPassword}`);
    document.querySelector('.popup .error').innerHTML = '';
    $findPassword.value = res.data;
  } catch (error) {
    console.error(error);
    document.querySelector('.popup .error').innerHTML = '존재하지 않는 이메일 입니다.';
  }
};

document.querySelector('.popup-button').onclick = async e => {
  e.preventDefault();
  await checkPassword();
};

document.querySelector('.popup-form').onsubmit = async e => {
  e.preventDefault();
  await checkPassword();
  $findPassword.blur();
};
