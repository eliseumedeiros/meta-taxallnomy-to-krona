import sys
import os
import pexpect
import getpass
#download site
import urllib.request

#NO PANDAS
import collections

path_input_file = ''
path_txmy = '/home/eliseu/Downloads/taxallnomy-master/get_lineage.pl'
analysis_type = 'r' #remote analysis is the defalt

def argv_validation(args):
	global path_input_file, path_txmy, analysis_type 
	if len(args) > 1:
		for i in range(len(args)):
			arg = args[i]
			if arg == '--file' or arg == '-f' or arg == '-file':
				path_input_file = args[i+1]

			elif arg == '--taxallnomy' or arg == '-tx' or arg == '-txmy':
				path_txmy = args[i+1]

			elif arg == '--type' or arg == '-t':
				analysis_type = args[i+1]
		return 0

	else:
		print('No arguments provided.')
		return -1

def local_analysis():
	global path_input_file, path_txmy, analysis_type 
	##### NO PANDAS
	#separate IDs from the original metagenomic file
	read_file = open(path_input_file, 'r')
	ids = []
	for line in read_file:
		id = line.split("\t")[2].replace("\n", "")
		if(id.isdigit()):
			ids.append(id)
	read_file.close()
	#save unique IDs file
	unique_ids = set(ids)
	write_file = open("ids_to_taxallnomy","w+")
	for line in unique_ids:
		write_file.write(str(line) + "\n")
	write_file.close()

	#get de user from local database
	user_database = input("Provide Mysql user from Taxallnomy database: ")
	password = getpass.getpass("Password: ")

	#execute command on Terminal
	command = "perl " + path_txmy + " -file ids_to_taxallnomy -out output_kaiju_taxallnomy -user "+ user_database 
	child = pexpect.spawn(command)
	child.sendline (password)

	#add count of IDs with taxonomic description in Krona input format
	tax_out = open('taxallnomy_analysis.out', 'r')
	final_result_krona = open('final_tax_input_krona', 'w+')
	id_counts = collections.Counter(ids)
	tax_out.readline() #file comment line
	tax_out.readline() #file comment line
	for line in tax_out:
		aux = line.split('\t')
		f_line = str(id_counts[aux[0]]) + line[len(aux[0])::]
		final_result_krona.write(f_line)
	final_result_krona.close()

	#remove auxiliary documents created in the process
	os.remove("ids_to_taxallnomy")
	os.remove("taxallnomy_analysis.out")

	print("Successfully executed")
	

def remote_analysis():
	global path_input_file, path_txmy, analysis_type 
	##### NO PANDAS
	#separate IDs from the original metagenomic file
	read_file = open(path_input_file, 'r')
	ids = []
	for line in read_file:
		id = line.split("\t")[2].replace("\n", "")
		if(id.isdigit()):
			ids.append(id)
	read_file.close()
	
	#gerar link
	beginning_link = "http://bioinfo.icb.ufmg.br/cgi-bin/taxallnomy/taxallnomy_multi.pl?txid="
	end_link = "&rank=main&format=tab"

	#generate unique IDs string
	unique_ids = set(ids)
	ids_to_link = ""
	for line in unique_ids:
		ids_to_link += line + ","
	mid_link = ids_to_link[:-1]

	link = beginning_link + mid_link + end_link

	#download taxallnomy results by link
	urllib.request.urlretrieve(link, "taxallnomy_analysis.out")

	#read the taxallnomy generated table
	tax_out = open('taxallnomy_analysis.out', 'r')
	final_result_krona = open('final_tax_input_krona', 'w+')
	id_counts = collections.Counter(ids)
	tax_out.readline() #file comment line
	tax_out.readline() #file comment line
	for line in tax_out:
		aux = line.split('\t')
		f_line = str(id_counts[aux[0]]) + line[len(aux[0])::]
		final_result_krona.write(f_line)
	final_result_krona.close()

	#remover documentos auxiliares criados no processo
	os.remove("taxallnomy_analysis.out")
	print("Successfully executed")

if argv_validation(sys.argv) != 0:
	print("There was a problem with the arguments provided.")
	exit()
if analysis_type == 'l':
	local_analysis()
else:
	remote_analysis()
