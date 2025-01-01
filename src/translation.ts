interface Translations {
  [key: string]: string;
}

const translations: Translations = {
  // index.html translations
  "Login": "Вход",
  "Username": "Потребителско име",
  "Password": "Парола",
  "Register": "Регистрация",
  "Email": "Имейл",
  "Submit": "Изпрати",
  "Close": "Затвори",

  // main.html translations
  "New Company:": "Нова компания:",
  "Team Name:": "Име на екипа:",
  "Team Members (comma separated):": "Членове на екипа (разделени със запетая):",
  "Update Company": "Актуализиране на компанията",
  "Create Team": "Създаване на екип",
  "Update Team": "Актуализиране на екипа",
  "Teams List": "Списък с екипи"
};

document.addEventListener('DOMContentLoaded', async () => {
  translatePage();
});

function translatePage() {
  const elements = document.querySelectorAll('*');
  
  elements.forEach((element) => {
    if (element.children.length === 0 && element.textContent) {
      const textContent = element.textContent.trim();
      if (translations[textContent]) {
        element.textContent = translations[textContent];
      }
    }
  });
}
