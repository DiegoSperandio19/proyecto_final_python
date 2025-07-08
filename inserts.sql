INSERT INTO role(
	id, name, scopes)
	VALUES ('1974ee3d-105d-4a74-9858-75d17c9822a0', 'client', Array['user:create', 'user:read', 'user:update', 'restaurant:read', 'table:read', 'reservation:create', 'reservation:update', 'reservation:delete', 'reservation:read', 'dish:read', 'preorder:create', 'preorder:read', 'preorder:delete']);


INSERT INTO role(
	id, name, scopes)
	VALUES ('b1fa2c3b-0bd5-4385-872a-f6267bf681c9', 'admin', Array['user:create', 'user:read', 'user:update', 'restaurant:read', 'restaurant:create', 'restaurant:update', 'restaurante:delete', 'table:read', 'table:create', 'table:update', 'table:delete', 'reservation:create', 'reservation:update', 'reservation:delete', 'reservation:read', 'dish:read', 'dish:create', 'dish:update', 'dish:delete', 'preorder:create', 'preorder:read', 'preorder:delete']);



INSERT INTO public."user"(
	id, email, hashed_password, name, role_id)
	VALUES ('dfd14982-eaff-4b82-9adc-47e2935a99d5', 'admin@gmail.com', '$2b$12$RJlU1ivTfKe3v9Sg1fAYvuMPTzftm0nZ825lZTp8ar.6aYk/izW86', 'admin_user', 'b1fa2c3b-0bd5-4385-872a-f6267bf681c9');




INSERT INTO public."user"(
	id, email, hashed_password, name, role_id)
	VALUES ('8b42b450-d9d0-46e7-831b-30941693bd17', 'client@gmail.com', '$2b$12$CLf8kdXicET/rc55ukOsduYHftuDlIvOsElqCVjq873TBIfqZgx5q', 'client_user', '1974ee3d-105d-4a74-9858-75d17c9822a0');
