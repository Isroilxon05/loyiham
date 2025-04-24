CREATE Table savat(ID int AUTO_INCREMENT PRIMARY key, Ism VARCHAR(50) , Familiya VARCHAR(50) , Manzil VARCHAR(200) , Tel_raqam VARCHAR(15) , Nomi VARCHAR(100) , Narxi VARCHAR(20));

CREATE Table mendagi_donirlar(ID int AUTO_INCREMENT PRIMARY key, Ism VARCHAR(50) , Familiya VARCHAR(50) , Manzil VARCHAR(200) , Tel_raqam VARCHAR(15) , Nomi VARCHAR(100) , Narxi VARCHAR(20));
drop TABLE kino;
CREATE Table kino(name VARCHAR(100), vide BLOB);
INSERT INTO kino(name, vide) VALUES('Kino1', LOAD_FILE(""C:\Users\asus\Videos\Captures\shaxsiy kormang.mp4""));

SELECT * FROM kino;