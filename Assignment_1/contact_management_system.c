//
//  main.c
//  Assignment_1
//
//  Created by yeonsoo choi on 06/09/2019.
//  Copyright © 2019 yeonsoo choi. All rights reserved.
//
#pragma warning(disable:4996)
#define _CRT_SECURE_NO_WARNINGS       // for protect 'fopen' error
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>


typedef struct List *list;
typedef list position;



struct List{                    //make struct
    char name[61];
    char phone[12];
    position next;
};



list create(list L){
    L = (list)malloc(sizeof(struct List));
    strcpy(L -> name,"name");
    strcpy(L -> phone,"phone");
    L->next = NULL;
    
    return L;
}





void insert(list L, char name[], char p_num[]){
    
    list tmp;
    tmp = malloc(sizeof(struct List));
    if(tmp == NULL){
        printf("insert error\n");
        exit(-1);
    }
    strcpy(tmp->name, name);
    strcpy(tmp->phone, p_num);
    
    tmp -> next = L -> next;
    L -> next = tmp;
}




int pnum_check(char p_num[]){   //to put 11 numbers start with '010'
    
    int number;
    char tmp;
   
    for(int i=0 ; i<3 ; i++){
        
        tmp = p_num[i];
        number = tmp - '0';
        
        if(number != i % 2){      // 0%2 ==0, 1%2 == 1, 2%2 == 0
            return 0;
        }
    }
    
    if(strlen(p_num) != 11){
        return 0;
    }
    
    return 1;
}






int check_same(char input_name[], char name_in_file[]){   // using in find() & delete()
                                                          // to search using just partial name
    int length = strlen(input_name);
    int count=0;
    
    for(int i=0 ; i<length ; i++){
        if(input_name[i] == name_in_file[i]){
            count++;
        }
    }
    
    if(count == length)
        return 1;
    else
        return 0;
}






list Find(list person, char name[]){        //find the name in the list person
    
    list tmp, tmp2;
    char finally_find[100];
    int check=0;
    tmp = person;
   
    while(tmp != NULL){
        
        if(check_same(name, tmp->name)){        //print all name matched with input_name
            check++;                            //for checking whether put whole name which is the only or not.
            printf("%2d.%s  ",check,tmp->name);
            printf("%s\n",tmp->phone);
            if(check==1){       //in case put whole name which is the only. to store it.
                tmp2 = tmp;
            }
        }
        tmp = tmp->next;
    }
    
    
    
    if(check >1){       //it means there are many options
        printf("Please collect Who you want to change (enter the name) : ");
        scanf("%s",finally_find);
        tmp = person;
        while(strcmp(finally_find, tmp->name)!=0){
            tmp = tmp->next;
        }
    }
    
    
    else if(check == 1){
        return tmp2;
    }
    
    return tmp;
    
}




list Find_pre(list person, char name[], int d_check){       //using in delete()
    list tmp,tmp2;
    char finally_find[100];
    int check=0;
    tmp = person;
    
    while(tmp->next != NULL){
           
        if(check_same(name, tmp->next->name)){
            check++;
            if(d_check != 2){
                printf("%2d.%s  ",check,tmp->next->name);
                printf("%s\n",tmp->next->phone);
            }
            if(check==1){
                tmp2 = tmp;
                
            }
        }
         
        tmp = tmp->next;
        
    }
    
       
    if(check >1){
        printf("Please collect Who you want to delete (enter the name) : ");
        scanf("%s",finally_find);
        tmp = person;
        while(strcmp(finally_find, tmp->next->name)!=0){
            tmp = tmp->next;
        }
    }
    
    else if(check == 1){
           return tmp2;
    }
       
    return tmp;
   
}





void Delete(list person, char name[], int d_check){
    list tmp,p;
    tmp = Find_pre(person, name, d_check);
    if(tmp->name != NULL){
        p = tmp->next;
        tmp -> next = p -> next;
        free(p);
    }
    else
        printf("delete fail. that's not in the list\n");
    
}





int main() {
    
    list person,tmp_list;
    
    FILE *fp = NULL;
    FILE *new_fp = NULL;
    
    int button;
    int file_exist;
    
    char str_tmp[100];
    char *tmp;          //to store
    char *file_name  = "2015005141_최연수.csv";
    char str[] = ",\r\n";    // use \r in .csv file but I use \n.
    
    file_exist = access(file_name, F_OK);

    person = create(person);        //create struct. this is header
    tmp_list = create(tmp_list);
    
    
    if(file_exist == 0)         //file exist
        fp = fopen( "2015005141_최연수.csv","r+" );
    else
        fp = fopen( "contact.csv","r+" );
    
    
    if ( fp != NULL){
       
        while ( fgets(str_tmp, 1024, fp) != NULL ){
            
            char name[61] = {'\0'};
            char p_number[12] = {'\0'};
            
            tmp = strtok(str_tmp, str);
            if(strcmp(tmp, "name")==0) continue;
            
            strcpy(name , tmp);
            
            tmp = strtok(NULL, str);
            strcpy(p_number , tmp);

            insert(person, name, p_number);
        }
    }
    
    else{
        printf("Open error\n");
        return 0;
    }
    
    fclose(fp);
    
    int cn =1;
    
    while(cn){
    
        printf("-----------------------\n");
        printf("1. find\n");
        printf("2. delete\n");
        printf("3. exit\n");
        printf("-----------------------\n");

        scanf("%d",&button);
        
        char input_name[100];           //to store update name and phone_number.
        char input_p_num[15] = { 0, };
        
        char remain_name[100]={'\0',};
        char remain_p_num[15]={'\0',};;

        int second_button;
        
        switch (button){
            case 1:
                printf("*Who do you want to find : ");
                scanf("%s",input_name);
                
                
                tmp_list = Find(person, input_name);
                
                if(tmp_list->name){
                    
                    printf("-----------------------\n");
                    printf("What do you want to change?\n");
                    printf("1.name\n");
                    printf("2.phone number\n");
                    printf("3.nothing\n");
                    printf("-----------------------\n");

                    scanf("%d",&second_button);
                    
                    if(second_button == 1){
                        printf("*please update %s's name : ", tmp_list->name);      //update the name
                        
                        char input_name[] = {'\0',};
                        scanf("%s",input_name);
                        strcpy(remain_p_num , tmp_list->phone);
                        Delete(person, tmp_list->name, 2);
                        insert(person, input_name, remain_p_num);
                    }
                    
                    else if(second_button == 2){
                        printf("*please update %s's phone number : ", tmp_list->name);      //update the phone_number
                        
                        char input_p_num[] = {'\0',};
                        scanf("%s",input_p_num);
                        
                        if(pnum_check(input_p_num)){
                            strcpy(remain_name, tmp_list->name);
                            Delete(person, tmp_list->name, 2);
                            insert(person, remain_name, input_p_num);
                            
                        }
                        
                        else{
                            printf("*please put 11 numbers start with 010\n");
                            break;
                        }
                    }
                    
                    
                    else if(second_button == 3){
                        break;
                    }
                    
                    
                    else{
                        printf("---Please enter 1 to 3---\n");
                        break;
                    }
                   
                    
                }
                else{
                    
                    printf("*%s is not in the list. please add\n",input_name);
                    printf("phone number : ");
                    scanf("%s", input_p_num);
                    
                    if(pnum_check(input_p_num)){
                        insert(person, input_name, input_p_num);
                    }
                    
                    else{
                        printf("*please put 11 numbers start with 010\n");
                        break;
                    }
                }
                
                break;
           
            
            case 2:
                printf("*who do you want to delete? : ");
                scanf("%s", input_name);
                Delete(person, input_name, 1);
                printf("------delete complete------\n");
                break;
            
            
            case 3:
                cn = 0;
                break;
            
            
            default:
                printf("-----please put 1 to 3-----\n");
                cn = 0;
                break;
        }
 
    
    }
    
    new_fp = fopen("2015005141_최연수.csv","w");       //remake the file to record updates.
        
    while(person != NULL){
        fputs(person->name, new_fp);
        fputs(",",new_fp);
        fputs(person->phone,new_fp);
        if(person->next !=NULL)
            fputs("\n",new_fp);
        person = person->next;
    }
    
    fclose( new_fp );
    
    return 0;
}

