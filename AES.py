'''
def plaintext_to_hex():	#평문의 각 문자를 16진수로 바꿔준다.
	hex_plaintext = ''	#16진수로 변환된 평문을 받을 빈 문자열
	plaintext = input("평문을 입력하시오 : ")
	
	for x in plaintext:
		hex_element = hex(ord(x))[2:]
		
		if len(hex_element)%2 != 0:	#평문의 각 문자를 16진수로 바꿀때 바이트에 맞게 딱딱 끊어준다. 15(10) = f(16) 0xf -> 0x0f
			hex_element = '0' + hex_element
			hex_plaintext += hex_element
		else:
			hex_plaintext += hex_element
		
	if int(len(hex_plaintext)/2)%16 != 0: #이과정을 통해서 평문이 16진수 이면서 32의배수인 문자열길이를 만족한다.
		padding_num = 16 - int(len(hex_plaintext)/2)%16 #패딩과정에서 X923패딩사용
		
		if padding_num >= 10:
			hex_plaintext += '00'*(padding_num - 1)+str(padding_num)
		else:
			hex_plaintext += '00'*(padding_num - 1)+'0'+str(padding_num)
			
	return hex_plaintext
	
a = plaintext_to_hex()
print(a)
'''
#=================================================================================================================================

def change_to_hex(text):#인자값으로 받은 문자열을 16진수로 변환에서 리턴하는 함수.
	hex_result = ''		#16진수로 변환된 결과를 받을 빈 문자열
	for x in text:
		hex_element = hex(ord(x))[2:]#hex함수를 써서 16진수로 변환하면 '0x'값이 붇는데 이를 지워준다.
		
		if len(hex_element)%2 != 0:	 #평문의 각 문자가 바이트 단위로 떨어지도록 16진수 짝수 자리가 되도록 한다.
			hex_element = '0' + hex_element
			hex_result += hex_element
		else:
			hex_result += hex_element
			
	return hex_result
	
	
def Padding(hex_plain):
	if int(len(hex_plain)/2)%16 != 0: #이과정을 통해서 평문이 16진수 이면서 32의배수인 문자열길이를 만족한다.
		padding_num = 16 - int(len(hex_plain)/2)%16 #패딩과정에서 X923패딩사용
		
		if padding_num >= 10:
			hex_plain += '00'*(padding_num - 1)+str(padding_num)
		else:
			hex_plain += '00'*(padding_num - 1)+'0'+str(padding_num)
			
	return hex_plain
	
#행렬을 모듈을 쓰지 않고 리스트로 구현할 것이다.
def make_matrix(hex_text):#4x4행렬을 만들어주는 함수이다.
	matrix = []			  #결과를 받을 리스트
	for block_num in range(int(len(hex_text)/32)):#128bits블록을 나눠서 나눠진 블록 만큼 반복
		tmp1 = []
		for row in range(4): 	#4x4행렬 이기떄문에 4번을 반복 
			tmp2 = []			#임시로 만든 리스트
			for column in range(4):
				tmp2.append(hex_text[block_num*32+row*2+column*8:block_num*32+row*2+column*8+2])
			tmp1.append(tmp2)
		matrix.append(tmp1)
			
	return matrix

	
def make_key_matrix():#함수이름 그대로 키를 받아서 행렬로만든다음 리턴하는 함수.
	while True:		  #무한루프
		key = input("16바이트 키를 입력하시오 : ")
		hex_key = change_to_hex(key)
		if len(hex_key)//2 == 16:	 #키의크기가 16바이트 128비트를 만족하면 무한루프를 빠져나간다.
			break
	key_matrix = make_matrix(hex_key)#위에서 선언한 행렬을 만들어주는 함수를 이용해서 행렬을 만든다.
	
	return key_matrix

	

def matrix_XOR(plain_matrix,key_matrix):#행렬끼리의 xor 연산을 담당하는 함수이다
	matrix = []
	for block in range(len(plain_matrix)):#block은 리스트 4개를 멤버로 가지는 리스트.
		tmp1 = []
		for row in range(4):
			tmp2 = []
			for column in range(4):
				XOR_result = hex(int(plain_matrix[block][row][column],16) ^ int(key_matrix[0][row][column],16))
				XOR_result = XOR_result[2:]
				
				if len(XOR_result)%2 != 0:
					XOR_result = '0' + XOR_result
				tmp2.append(XOR_result)
			tmp1.append(tmp2)
		matrix.append(tmp1)
	
	return matrix
	
#확인하는 과정
hex_plain = change_to_hex('z') #평문을 입력해준다.
hex_plain = Padding(hex_plain) #입력한 평문을 블록의 크기에맞게 패딩해준다.

plain_matrix = make_matrix(hex_plain)#16진수로 변환된 평문을 4x4행렬로 만들어준다.
print(plain_matrix)

key_matrix = make_key_matrix() #키를 만들고 16진수로 구성된 4x4행렬을 리턴
print(key_matrix)


XOR_result = matrix_XOR(plain_matrix,key_matrix) #키행렬과 평문행렬을 XOR해서 리턴해주는 과정
print(XOR_result)
