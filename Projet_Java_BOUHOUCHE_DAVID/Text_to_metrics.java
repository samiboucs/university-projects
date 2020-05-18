package text_to_metrics;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Text_to_metrics {

	
	public Hashtable<String,Integer> hPOS=new Hashtable<String,Integer>();
	public Hashtable<String,Integer> hLem=new Hashtable<String,Integer>();
	public Hashtable<String,Integer> hmots=new Hashtable<String,Integer>(); 
	public ArrayList<String> lignes=new ArrayList<String>();
	public ArrayList<String> formes=new ArrayList<String>();
	public ArrayList<String> POS=new ArrayList<String>();
	public ArrayList<String> lemmes=new ArrayList<String>();
	public ArrayList<String> hformes=new ArrayList<String>();
	public int nbLines;
	public int nbCar;
		
	/*---------- …tiquetage par TreeTagger ----------*/
	public void run_ttg() 
	{
	
		Runtime runtime = Runtime.getRuntime();
		String[] param = {"py", "ttw.py", "sami"};
		try {
			final Process process = runtime.exec(param);
			
			BufferedReader reader = new BufferedReader(
					new InputStreamReader(
							process.getInputStream()));
			
			String ligne = "";
			
			try {
				//Lecture des lignes
				while ((ligne = reader.readLine()) != null) {
					System.out.println(ligne);
				}
			} finally {
				reader.close();
			}
			
		} catch(IOException e) {
			System.out.println("Appel externe impossible !");
		}
		
	}
	
	public int car_count(){

		{
			
			String ligne;
			try {
				BufferedReader file = new BufferedReader(new FileReader(new File("fichier.txt")));
				System.out.println("\nLe fichier texte existe !\n");
				while ((ligne = file.readLine())!=null) { // Lecture d'une ligne 
					nbCar+=ligne.length();;
				}
				file.close();
				
			} 
			catch(FileNotFoundException e) {
				// Le fichier n'a pas ÈtÈ trouvÈ !
				System.out.println("Le fichier texte n'existe pas !\n");
			
			} catch (IOException e) {
				// La lecture dans le fichier a ÈchouÈ !
				System.out.println("…chec de la lecture du fichier texte !\n");
				
			}
		} return nbCar;
	}
	
	public int line_count(){
		{
			
			String ligne;
			
			try {
				BufferedReader file = new BufferedReader(new FileReader(new File("fichier.txt")));
				System.out.println("\nLe fichier texte existe !\n");
				nbLines = 0;
				while ((ligne = file.readLine())!=null) { // Lecture d'une ligne 
					nbLines++;
					
				}
				file.close();
				
			} 
			catch(FileNotFoundException e) {
				// Le fichier n'a pas ÈtÈ trouvÈ !
				System.out.println("Le fichier texte n'existe pas !\n");
			
			} catch (IOException e) {
				// La lecture dans le fichier a ÈchouÈ !
				System.out.println("…chec de la lecture du fichier texte !\n");
				
			}
		}	
		return nbLines;
		 }
		/*---------- Lecture du fichier ÈtiquetÈ ----------*/
	 public ArrayList<String> read_csv()
	 {
		String ligne;
		nbCar = 0;
		try {
			BufferedReader file = new BufferedReader(new FileReader(new File("tags.csv")));
			System.out.println("\nLe fichier existe !\n");
			while ((ligne = file.readLine())!=null) { // Lecture d'une ligne
				lignes.add(ligne);
			
			}
			file.close();
			
		} catch(FileNotFoundException e) {
			// Le fichier n'a pas ÈtÈ trouvÈ !
			System.out.println("Le fichier n'existe pas !\n");
		
		} catch (IOException e) {
			// La lecture dans le fichier a ÈchouÈ !
			System.out.println("…chec de la lecture !\n");
			
		}
		
	 return lignes;
	 }
		
	
	 public void parse(ArrayList<String> lignes)
	 {
		/*---------- CrÈation d'un tableau ‡ 3 dimensions ----------*/
		ArrayList<String> elements= new ArrayList<String>();
		int i = 0;
		for (i=0;i<lignes.size();i=i+1) {
			String current =  lignes.get(i);
			elements.add(current);
			//String lemme = list[i];
			//lemmes.add(lemme);
			String[] arrOfStr = current.split("\t",3); 
			if (arrOfStr.length==3) {
				formes.add(arrOfStr[0]);
				POS.add(arrOfStr[1]); 
				lemmes.add(arrOfStr[2]); 
			}
			
		}
		
	 }
		
	 /*---------- Calcul du nombre de phrases ----------*/	
	public int sent_count(ArrayList<String> POS)
	{
		int cptP = 0;
		Pattern pattern;
	    Matcher matcher;
		pattern = Pattern.compile("SENT");
	    matcher = pattern.matcher(POS.toString());
	    while(matcher.find()) {
		    //System.out.println(matcher.group());
	        cptP++;
	    }
	    System.out.println("Le texte contient : "+cptP+" phrases\n");
	 	return cptP;
	}
	
	/*---------- Calcul du nombre de tokens ----------*/
	public int tok_count(ArrayList<String> formes)
	{	
		int cptT = 0;
		Pattern pattern1;
	    Matcher matcher1;
		pattern1 = Pattern.compile("[A-Z|a-z|‡‚‰ÈËÍÎÓÔˆÙ˘˚¸Á¿¬ƒ…» ÀŒœ‘÷Ÿ€‹«]+(\\.|-|')?([A-Z|a-z|‡‚‰ÈËÍÎÓÔˆÙ˘˚¸Á¿¬ƒ…» ÀŒœ‘÷Ÿ€‹«]+)?");
	    //pattern1 = Pattern.compile("\\w+(?=-(?:t|je|tu|il|elle|on|nous|vous|ils|elles|eux|mÍme|mÍmes|lui|le|la|leur|y|en|moi|toi)\b)|-|[\\w-]+\\'?|[^ ]");
		matcher1 = pattern1.matcher(formes.toString());
		while(matcher1.find()) {
		    //System.out.println(matcher1.group());
			hformes.add(matcher1.group());
		    cptT++;
		}
	    System.out.println("Le texte contient : "+cptT+" tokens\n");
	    return cptT;
	}

/*----------------- Calcul des occurrences de chaque ÈlÈment -----------------*/	    
	public Hashtable<String,Integer> tok_occ(ArrayList<String> hformes)
	{
	    
		for (String m:hformes) {
			if (hmots.containsKey(m)) {
				hmots.put(m,hmots.get(m)+1);
			} else {
				hmots.put(m,1);
			}
		}
		return hmots;
	}
		
	public Hashtable<String,Integer> POS_occ(ArrayList<String> POS)
	{
		Hashtable<String,Integer> hPOS = new Hashtable<String,Integer>();
		for (String m:POS) {
			if (hPOS.containsKey(m)) {
				hPOS.put(m,hPOS.get(m)+1);
			} else {
				hPOS.put(m,1);
			}
		}
		return hPOS;
   }
	
	public Hashtable<String,Integer>lem_occ(ArrayList<String> lemme)
	{ 
		Hashtable<String,Integer> hLem = new Hashtable<String,Integer>();
		for (String m:lemmes) {
			if (hLem.containsKey(m)) {
				hLem.put(m,hLem.get(m)+1);
			} else {
				hLem.put(m,1);
			}
		}
		return hLem;
	}
	
	/*-------------------- Ècriture|affichage des rÈsultats ---------- ---------- */
	public void tok_occ_write(Hashtable<String,Integer>hmots)
	{ 
		Enumeration<String> e = hmots.keys();
		while (e.hasMoreElements()) {
			String cle = e.nextElement();
			System.out.println(cle+" : "+hmots.get(cle));
		}		
		System.out.println("\n");
	}	
	
	public void POS_occ_write(Hashtable<String,Integer> hPOS)
	{ 
		Enumeration<String> p = hPOS.keys();
		while (p.hasMoreElements()) {
			String cle = p.nextElement();
			System.out.println(cle+" : "+hPOS.get(cle));
		}		
		System.out.println("\n");
	}
		
	
	public void lem_occ_write(Hashtable<String,Integer> hLem)
	{ 
		Enumeration<String> l = hLem.keys();
		while (l.hasMoreElements()) {
			String cle = l.nextElement();
			System.out.println(cle+" : "+hLem.get(cle));
		}
		
		System.out.println("\n");
	}
	
	public void process(){
		run_ttg();
		read_csv();
		parse(lignes);
		sent_count(POS);
		tok_count(formes);
		tok_occ(hformes);
		POS_occ(POS);
		lem_occ(lemmes);
		lem_occ_write(hLem);
		POS_occ_write(hPOS);
		lem_occ_write(hmots);
	}

}

