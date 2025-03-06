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
  "Teams List": "Списък с екипи",
  "Update User Role": "Актуализиране на ролята на потребителя",
  "Manage Materials": "Управление на материали",
  "Recruit": "Набиране",
  "Sign out": "Изход",
  "Support": "Поддръжка",
  "Your name:": "Вашето име:",
  "What's your problem:": "Какъв е вашият проблем:",
  "Send": "Изпрати",
  "Chat": "Чат",
  "Message here...": "Съобщение тук...",
  "New Chat": "Нов чат",
  "Your Chats:": "Вашите чатове:",
  "Select participants:": "Изберете участници:",
  "Selected Participants:": "Избрани участници:",
  "Create Chat": "Създаване на чат",
  "Add Material": "Добавяне на материал",
  "Material Name:": "Име на материала:",
  "Material Quantity:": "Количество материал:",
  "Materials List:": "Списък с материали",
  "Assign Task": "Възлагане на задача",
  "Task Name:": "Име на задачата:",
  "Task Description:": "Описание на задачата:",
  "Level:": "Ниво:",
  "Call Gemini": "Обадете се на Gemini",
  "Create Teams": "Създаване на екипи",
  "Update role": "Актуализиране на ролята",
  "Update Companys": "Актуализиране на компании",
  "Update Teams": "Актуализиране на екипи",
  "Update Materials": "Актуализиране на материали",
  "Update Tasks": "Актуализиране на задачи",
  "Update Users": "Актуализиране на потребители",
  "Updare Role": "Актуализиране на роли",
  "Participants": "Участници",
  "Chat Name:": "Име на чата:",
  "Chat Description:": "Описание на чата:",
  "Chat Level:": "Ниво на чата:",
  "Chat Participants:": "Участници в чата:",
  "Chat Messages:": "Съобщения в чата:",
  "Chat Name": "Име на чата",
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
