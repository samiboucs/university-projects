//Auteur : Emerson Raniere
//GitHub Jena Repository : https://github.com/EmersonRaniere/Jena
//Adapté par Sami BOUHOUCHE et Nicolas Leewys DAVID

package jena_rdf;

import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.rdf.model.Literal;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.util.FileManager;

public class Main {

	public static void main(String[] args) {
		sparqlTest();

	}
	
	static void sparqlTest(){
		FileManager.get().addLocatorClassLoader(Main.class.getClassLoader());
		Model model = FileManager.get().loadModel("/Users/Nemesis/Desktop/longit.rdf");
		
		String queryString = 
						"PREFIX rdf: <http://www.semanticweb.org/corpuscol/ontologies/2019/1/longit#>" +
						"SELECT * WHERE { " +
						"?production rdf:name ?x ."+
						"?production rdf:f_measure ?f_measure."+
				        "FILTER( ?f_measure = \"0.45\")"+
						"}";
		
		Query query = QueryFactory.create(queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		
		try {
			org.apache.jena.query.ResultSet results = qexec.execSelect();
			System.out.println("Production(s) concernée(s) : ");
			while ( results.hasNext() ){
				QuerySolution solution = results.nextSolution();
				Literal name = solution.getLiteral("x");
				System.out.println(name);
			}
		} 
		
		finally {
			qexec.close();
		}		
	}
}
