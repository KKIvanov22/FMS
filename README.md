## Необходими зависимости
- [Python](https://www.python.org/downloads/) (препоръчително: последната стабилна версия)
- [Node.js](https://nodejs.org/) и npm (препоръчително: последната стабилна версия)
- TypeScript

## Инсталация
1. Изтеглете и инсталирайте [Python](https://www.python.org/downloads/).
2. Добавете Python в PATH по време на инсталацията.
3. Изтеглете и инсталирайте [Node.js](https://nodejs.org/), което включва npm.
4. Инсталирайте TypeScript с командата:

   ```sh
   npm install -g typescript
   ```
##Инсталиране на проекта от GitHub ZIP

1. Отидете в GitHub хранилището на проекта.

2. Натиснете бутона "Code" и изберете "Download ZIP".

3. Разархивирайте изтегления ZIP файл в желаната директория.

4. Влезте в разархивираната папка
   
## Стартиране на приложението
1. Създайте виртуална среда:

   ```sh
   python -m venv venv
   ```

2. Активирайте виртуалната среда:

   ```sh
   venv\Scripts\activate
   ```

3. Ако получите грешка при разрешенията, изпълнете:

   ```sh
   Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
   ```

4. Инсталирайте необходимите Python зависимости:

   ```sh
   pip install -r requirements.txt
   ```

5. Инсталирайте Electron:

   ```sh
   npm install electron
   ```

6. Стартирайте приложението:

   ```sh
   python app.py
   ```

7. След приключване изключете виртуалната среда:

   ```sh
   deactivate
   ```

## Допълнителна информация
Ако срещнете проблеми, уверете се, че всички зависимости са инсталирани правилно и че използвате актуални версии на Python и Node.js.
