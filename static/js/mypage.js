const render = (() => {
  window.onload = async () => {
    try {
      const { data: user } = await axios.get('/checkAuth');

      if (user) {
        document.querySelector('.mypage-form-email > input').value = user.email;
        document.querySelector('.mypage-form-name > input').value = user.name;
        document.querySelector('.mypage-form-phone > input').value = user.phone;
      }
    } catch (e) {
      console.error(e);
    }
  };
})();

document.querySelector('.edit-profile-button').onclick = () => {
  window.location.href = '/mypage_edit';
};

document.querySelector('.form-back').onclick = async () => {
  try {
    const check = await axios.get('/users/logout');
    if (check.status === 204) window.location.href = '/signin';
  } catch (e) {
    console.error(e);
  }
};
