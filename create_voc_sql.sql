-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        11.2.2-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- userlist 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `userlist` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci */;
USE `userlist`;

-- 테이블 userlist.board 구조 내보내기
CREATE TABLE IF NOT EXISTS `board` (
  `id` int(11) NOT NULL DEFAULT 0,
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `wdate` timestamp NULL DEFAULT current_timestamp(),
  `view` int(11) DEFAULT 0,
  `post_password` int(11) DEFAULT NULL,
  `majorseq` int(11) DEFAULT NULL,
  `minorseq` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- 테이블 데이터 userlist.board:~11 rows (대략적) 내보내기
INSERT IGNORE INTO `board` (`id`, `name`, `password`, `title`, `content`, `wdate`, `view`, `post_password`, `majorseq`, `minorseq`) VALUES
	(1, 'gilsu.yoon', 'Gilsu3320!', 'adfa', 'dfadfadf', '2024-01-25 23:15:24', 5, NULL, NULL, NULL),
	(2, 'gilsu.yoon', 'Gilsu3320!', 'adfadfadf', 'adfadfadfadf', '2024-01-25 23:18:17', 0, NULL, NULL, NULL),
	(3, 'gilsu.yoon', 'Gilsu3320!', 'adfadfa', 'dfadfadfa', '2024-01-25 23:18:24', 2, NULL, NULL, NULL),
	(4, 'gilsu.yoon', 'Gilsu3320!', 'adfadfadfadfad', 'fadfadfadf', '2024-01-25 23:19:03', 23, NULL, NULL, NULL),
	(5, 'gilsu.yoon', 'Gilsu3320!', 'adfad', 'fadfadfa', '2024-01-26 01:18:58', 8, NULL, NULL, NULL),
	(6, 'gilsu.yoon', 'Gilsu3320!', 'adfadfadf', 'adfadf', '2024-01-26 02:06:46', 75, NULL, NULL, NULL),
	(7, 'gilsu.yoon', 'Gilsu3320!', '1231', '2313', '2024-01-26 02:44:00', 21, 123, NULL, NULL),
	(8, 'gilsu.yoon', 'Gilsu3320!', '123', '13', '2024-01-26 06:51:49', 5, 12, NULL, NULL),
	(9, 'gilsu.yoon', 'Gilsu3320!', '123123', '123123\r\n\r\nadfadfad', '2024-01-29 23:06:15', 27, 1234, NULL, NULL),
	(10, 'gilsu.yoon', 'Gilsu3320!', '123123', '1231231', '2024-01-31 00:56:54', 12, 1234, NULL, NULL),
	(11, 'gilsu.yoon', 'Gilsu3320!', 'asdfad', 'fadfadf', '2024-01-31 02:29:37', 0, 1234, NULL, NULL),
	(12, 'gilsu.yoon', 'Gilsu3320!', '12313123', '123123', '2024-01-31 02:29:51', 5, 1231, NULL, NULL);

-- 테이블 userlist.comments 구조 내보내기
CREATE TABLE IF NOT EXISTS `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `wdate` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- 테이블 데이터 userlist.comments:~11 rows (대략적) 내보내기
INSERT IGNORE INTO `comments` (`id`, `post_id`, `comment`, `user_name`, `wdate`) VALUES
	(1, 3, 'ㅁㅇㄻㅇㄻㅇㄹ', 'gilsu.yoon', '2024-01-25 23:29:10'),
	(2, 4, 'ㄴㅀㄴㅀㄴㅀㄹ', 'gilsu.yoon', '2024-01-25 23:40:01'),
	(3, 4, 'ㅁㅇㄻㅇㄹ', 'gilsu.yoon', '2024-01-25 23:41:03'),
	(4, 4, 'ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ', 'gilsu.yoon', '2024-01-25 23:41:10'),
	(5, 7, 'ㅁㅇㄻㅇㄹ', 'gilsu.yoon', '2024-01-26 04:22:57'),
	(93, 9, '123123123', 'gilsu.yoon', '2024-01-31 00:56:47'),
	(94, 9, '123123', 'gilsu.yoon', '2024-01-31 00:56:48');

-- 테이블 userlist.files 구조 내보내기
CREATE TABLE IF NOT EXISTS `files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `upload_date` timestamp NULL DEFAULT current_timestamp(),
  `post_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- 테이블 데이터 userlist.files:~1 rows (대략적) 내보내기
INSERT IGNORE INTO `files` (`file_id`, `file_name`, `file_path`, `upload_date`, `post_id`) VALUES
	(2, 'HGX_CN_-__2.pdf', 'C:\\Users\\L0140\\Desktop\\flask-board-practice-master\\uploads\\HGX_CN_-__2.pdf', '2024-01-25 23:19:03', 4);

-- 테이블 userlist.major 구조 내보내기
CREATE TABLE IF NOT EXISTS `major` (
  `MajorName` varchar(100) DEFAULT NULL,
  `MajorSeq` int(11) NOT NULL,
  `Remark` varchar(100) DEFAULT NULL,
  `MajorType` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- 테이블 데이터 userlist.major:~3 rows (대략적) 내보내기
INSERT IGNORE INTO `major` (`MajorName`, `MajorSeq`, `Remark`, `MajorType`) VALUES
	('OA', 1, '대분류', 1),
	('SoftWare', 2, '대분류', 1),
	('Solution', 3, '대분류', 1);

-- 테이블 userlist.minor 구조 내보내기
CREATE TABLE IF NOT EXISTS `minor` (
  `MinorName` varchar(100) DEFAULT NULL,
  `MinorSeq` int(11) NOT NULL,
  `Remark` varchar(100) DEFAULT NULL,
  `MajorSeq` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- 테이블 데이터 userlist.minor:~6 rows (대략적) 내보내기
INSERT IGNORE INTO `minor` (`MinorName`, `MinorSeq`, `Remark`, `MajorSeq`) VALUES
	('전자결재', 1, '중분류', 2),
	('유선', 2, '중분류', 3),
	('메일', 3, '중분류', 3),
	('모니터', 4, '중분류', 1),
	('복합기', 5, '중분류', 1),
	('데스크톱', 6, '중분류', 1);

-- 테이블 userlist.tbl_user 구조 내보내기
CREATE TABLE IF NOT EXISTS `tbl_user` (
  `user_name` varchar(20) NOT NULL,
  `user_password` varchar(500) NOT NULL,
  `user_password1` varchar(200) NOT NULL,
  PRIMARY KEY (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- 테이블 데이터 userlist.tbl_user:~2 rows (대략적) 내보내기
INSERT IGNORE INTO `tbl_user` (`user_name`, `user_password`, `user_password1`) VALUES
	('gilsu.yoon', 'pbkdf2:sha256:600000$WBJR80Uof3nekg02$d1980f1584050d338eb7efd33687ff6f4c95ae8a39b0335ed5704fae01140a4f', 'Gilsu3320!'),
	('gilsu.yoon1', 'pbkdf2:sha256:600000$F9eqMVK7DfAOGxIA$cd63ed57cf8b1ac7a611e36e528e79820110f46ddb148c1655712f37136da29b', 'Gilsu3320!@');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
