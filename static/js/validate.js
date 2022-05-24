const $iconSuccess = document.querySelectorAll('.icon-success');
const $iconError = document.querySelectorAll('.icon-error');
const $error = document.querySelectorAll('.error');

const iconChange = (index, isError) => {
  if (isError) {
    $iconSuccess[index].classList.add('hidden');
    $iconError[index].classList.remove('hidden');
  } else {
    $iconSuccess[index].classList.remove('hidden');
    $iconError[index].classList.add('hidden');
  }
};

const countCorrectInput = (arr, index, btn) => {
  const cnt = arr.filter(idx => !$iconSuccess[idx].classList.contains('hidden')).length;

  if (cnt === arr.length) btn.removeAttribute('disabled');
};

const activeSubmitButton = (reg, index, btn) => {
  if (reg) btn.setAttribute('disabled', '');
  else {
    countCorrectInput(
      [...$iconSuccess].map((_, i) => i),
      index,
      btn
    );
  }
};

const checkIsCorrectForm = (reg, index, msg, btn, beforeCheck = true) => {
  if (beforeCheck) iconChange(index, reg);

  $error[index].textContent = reg ? msg : '';
  $error[index].style.color = '#ed2553';
  activeSubmitButton(reg, index, btn);
};

export default {
  emailValidate(value, index, button, beforeCheck) {
    const regEmail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;

    return checkIsCorrectForm(!regEmail.test(value), index, '이메일 형식에 맞게 입력해 주세요.', button, beforeCheck);
  },

  nameValidate(value, index, button) {
    const regName = /^[^\s]{1,}$/;

    return checkIsCorrectForm(!regName.test(value), index, '이름을 입력해 주세요.', button);
  },

  phoneValidate(value, index, button) {
    const regPhone = /^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$/;

    return checkIsCorrectForm(!regPhone.test(value), index, '전화번호를 형식에 맞게 입력해 입력해 주세요.', button);
  },

  // password validate
  passwordValidate(value, index, button) {
    const regPassword = /^[A-Za-z0-9]{6,12}$/;

    return checkIsCorrectForm(!regPassword.test(value), index, '영문 또는 숫자를 6~12자 입력하세요.', button);
  },

  passwordConfirmValidate(value, index, button) {
    return checkIsCorrectForm(value, index, '비밀번호가 올바르지 않습니다.', button);
  },
};
