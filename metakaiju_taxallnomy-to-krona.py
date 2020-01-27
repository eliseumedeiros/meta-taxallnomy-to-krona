import sys
import os
import pandas as pd
import pexpect
import getpass
# #baixar site
import urllib.request

path_input_file = ''
path_txmy = ''
analysis_type = 'r' #remote analysis is the defalt

def argv_validation(args):
	global path_input_file, path_txmy, analysis_type 
	if len(args) > 1:
		for i in range(len(args)):
			arg = args[i]
			if arg == '--file' or arg == '-f':
				path_input_file = args[i+1]
			elif arg == '--taxallnomy' or arg == '-txm':
				path_txmy = args[i+1]
			elif arg == '--type' or arg == '-t':
				analysis_type = args[i+1]
			elif arg == '--local' or arg == '-l':
				analysis_type = 'l'
			elif arg == '--remote' or arg == '-r':
				analysis_type = 'r'
		return 0

	else:
		print('No arguments provided.')
		return -1

def local_analysis():
	global path_input_file, path_txmy, analysis_type 
	#read table output from Kaiju
	names = ["classified","name", "id", "size", "others_ids", "others", "prot"]
	result_kaiju = pd.read_csv(path_input_file,sep="\t", header=None, names=names)
	
	#save file of IDs taxallnomy
	input_taxallnomy = pd.Series(result_kaiju.id.unique())
	input_taxallnomy.to_csv("ids_to_taxallnomy", header=False, index=None)
	
	#get de user from local database
	user_database = input("Provide Mysql user from Taxallnomy database: ")
	password = getpass.getpass("Password: ")
	
	#execute command on Terminal
	command = "perl " + path_txmy + " -file ids_to_taxallnomy -out taxallnomy_analysis.out -user "+ user_database 
	child = pexpect.spawn(command)
	child.sendline (password)
	child.wait()
	#read the taxallnomy generated table
	name = "id superkingdom  kingdom  phylum  subphylum  superclass  class  subclass  superorder  order  suborder  superfamily  family  subfamily  genus  subgenus  species    subspecies"
	out_kaiju_taxallnomy = pd.read_csv("taxallnomy_analysis.out", sep="\t", header=None, names=name.split())
	out_kaiju_taxallnomy = out_kaiju_taxallnomy.drop(out_kaiju_taxallnomy.index[:2]).reset_index()

	#count corruence of IDs
	counts_kaiju_krona = result_kaiju.groupby('id').size().reset_index(name='count')

	#unify description table with counted ocurruence table
	counts_kaiju_krona.id = counts_kaiju_krona.id.astype('str')
	out_kaiju_taxallnomy.id = out_kaiju_taxallnomy.id.astype('str')
	krona_kaiju_table = pd.merge(counts_kaiju_krona, out_kaiju_taxallnomy, on="id", how="inner")

	krona_kaiju_table.drop(['id', 'index'], axis=1).to_csv('input_kaiju_krona', sep='\t', header=False, index=None)
	#remover documentos auxiliares criados no processo
	os.remove("ids_to_taxallnomy")
	os.remove("taxallnomy_analysis.out")

	print("Successfully executed")

def remote_analysis():
	global path_input_file, path_txmy, analysis_type 
	#read table output from Kaiju
	names = ["classified","name", "id", "size", "others_ids", "others", "prot"]
	result_kaiju = pd.read_csv(path_input_file,sep="\t", header=None, names=names)
	
	#save file of IDs taxallnomy
	input_taxallnomy = pd.Series(result_kaiju.id.unique())
	input_taxallnomy.to_csv("ids_to_taxallnomy", header=False, index=None)

	#gerar link
	beginning_link = "http://bioinfo.icb.ufmg.br/cgi-bin/taxallnomy/taxallnomy_multi.pl?txid="
	end_link = "&rank=main&format=tab"
	ids_taxallnomy = pd.read_csv("ids_to_taxallnomy", header=None)
	mid_link = ids_taxallnomy.to_string(header=False, index=False).replace("\n",",").replace(' ', '')

	link = beginning_link + mid_link + end_link
	#print(link)
	#baixar resultados taxallnomy pelo link
	urllib.request.urlretrieve(link, "taxallnomy_analysis.out")

	#read the taxallnomy generated table
	name = "id superkingdom  kingdom  phylum  subphylum  superclass  class  subclass  superorder  order  suborder  superfamily  family  subfamily  genus  subgenus  species    subspecies"
	out_kaiju_taxallnomy = pd.read_csv("taxallnomy_analysis.out", sep="\t", header=None, names=name.split())
	out_kaiju_taxallnomy = out_kaiju_taxallnomy.drop(out_kaiju_taxallnomy.index[:2]).reset_index()
	
	#count corruence of IDs
	counts_kaiju_krona = result_kaiju.groupby('id').size().reset_index(name='count')

	#unify description table with counted ocurruence table
	counts_kaiju_krona.id = counts_kaiju_krona.id.astype('str')
	out_kaiju_taxallnomy.id = out_kaiju_taxallnomy.id.astype('str')
	krona_kaiju_table = pd.merge(counts_kaiju_krona, out_kaiju_taxallnomy, on="id", how="inner")

	krona_kaiju_table.drop(['id', 'index'], axis=1).to_csv('input_kaiju_krona', sep='\t', header=False, index=None)
	#remover documentos auxiliares criados no processo
	os.remove("ids_to_taxallnomy")
	os.remove("taxallnomy_analysis.out")

	print("Successfully executed")


if argv_validation(sys.argv) != 0:
	print("There was a problem with the arguments provided.")
	exit()

if analysis_type == 'l':
	local_analysis()
else:
	remote_analysis()
